from __future__ import absolute_import

from supernova.celery import app
from datetime import timedelta
from http.client import BadStatusLine
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import redis

from websites.models import Domain, Webpage, Link


# Debug task
@app.task
def add(x, y):
    return x + y


r_server = redis.Redis('localhost')



def extract_domain_and_path(url):
    url_parsed = re.match('^(?:https?://)?(?P<domain>[a-z0-9\.]+)(?P<uri>[^#\?]+)?.*$', url)
    domain_name = url_parsed.group('domain').lower()
    try:
        uri_path = url_parsed.group('uri')
        if uri_path[-1] == '/':
            uri_path = uri_path[:-1]
    except IndexError:
        uri_path = '/'
    return domain_name, uri_path


def get_domain_and_webpage_models(domain_name, uri_path):
    domain = Domain.objects.get_or_create(name=domain_name, pagerank=0)[0]
    domain.save()
    webpage = Webpage.objects.get_or_create(domain=domain, path=uri_path)[0]
    webpage.save()
    return domain, webpage


def create_link(start, end):
    if start is not None:
        Link.objects.get_or_create(start=start, end=end)[0].save()


def download_and_create_html_object(url):
    print('Downloading page ...')
    try:
        html_src = urlopen(url).read()
    except BadStatusLine:
        print('Exception: BadStatusLine')
        return None
    return BeautifulSoup(html_src)


def parse_html_object(soup):
    print('Parsing page ...')
    result = dict()
    meta_keywords = soup.head.find('meta', attrs={'name': 'Keywords'})
    meta_description = soup.head.find('meta', attrs={'name': 'Description'})

    result['title'] = soup.title.string
    result['description'] = meta_description.attrs['content']
    result['keywords'] = meta_keywords.attrs['content']
    result['content'] = soup.get_text()
    return result


def get_redis_key(url):
    return 'crawler_' + url


def crawl_links(urls, domain_name, uri_path, webpage):
    print('Delaying other pages to crawl and parse ...')
    for url in urls:
        if url[0] == '/':
            url = domain_name + url
        elif url.find('.') == -1:  # dot is allowed only in domain name
            url = domain_name + uri_path + ('/' if uri_path[-1] != '/' else '') + url
        if not url.startswith('http://'):
            url = 'http://' + url

        url_pref_len = len('https://')
        redis_key = get_redis_key(url[url_pref_len:])
        if r_server.get(redis_key) != 'Cached':
            crawl_and_parse.delay(url, webpage)
        else:
            _, son_webpage = get_domain_and_webpage_models(extract_domain_and_path(url))
            create_link(start=webpage, end=son_webpage)


@app.task
def crawl_and_parse(url, referrer_webpage=None):
    print('Parsing {url} ...'.format(url=url))
    print('Refereer: {0}'.format(referrer_webpage))

    domain_name, uri_path = extract_domain_and_path(url)
    domain, webpage = get_domain_and_webpage_models(domain_name, uri_path)
    create_link(start=referrer_webpage, end=webpage)

    # connect to cache server and set some variables
    redis_key = get_redis_key(domain_name + uri_path)
    if r_server.get(redis_key) == 'Cached':
        print('Already parsed!')
        return True
    r_server.setex(redis_key, 'Cached', timedelta(hours=1))
    r_server.incr('started_crawling')

    print('Parse statistics (ended / started): {0} / {1}'.format(
                                                    r_server.get('ended_crawling'),
                                                    r_server.get('started_crawling')))

    soup = download_and_create_html_object(url)
    if soup is None:
        return False
    parsed_data = parse_html_object(soup)

    # save data
    print('Saving data to database ...')
    domain.save()
    print('parsed_data: ' + str(parsed_data))
    for k, v in parsed_data.items():
        webpage.__setattr__(k, v)
    webpage.save()

    # Refresh link list
    #Link.objects.filter(start=webpage).delete()
    # FIXME force line above to work correctly!

    # crawl rest of pages
    urls = [a['href'] for a in soup.find_all('a')]
    crawl_links(urls, domain_name, uri_path, webpage)

    r_server.incr('ended_crawling')
    print('Done.')
    return True