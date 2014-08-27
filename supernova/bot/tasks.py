from __future__ import absolute_import


from bot.celery import app
from datetime import timedelta
from http.client import BadStatusLine
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import redis


# Debug task
@app.task
def add(x, y):
    return x + y


# TODO must be finished by mrowqa
@app.task
def crawl_and_parse(url):
    from websites.models import Domain, Webpage

    print('Parsing {url} ...'.format(url=url))

    # extract domain name and uri path from url
    url_parsed = re.match('^(?:https?://)?(?P<domain>[a-z0-9\.]+)(?P<uri>[^#\?]+)?.*$', url)
    domain_name = url_parsed.group('domain').lower()
    try:
        uri_path = url_parsed.group('uri')
        if uri_path[-1] == '/':
            uri_path = uri_path[:-1]
    except IndexError:
        uri_path = '/'

    # connect to cache server
    print('Connecting to Redis server ...')
    redis_key = domain_name + uri_path
    r_server = redis.Redis('localhost')
    if r_server.get(redis_key) == 'Cached':
        print('Already parsed!')
        return True
    r_server.setex(redis_key, 'Cached', timedelta(hours=1))

    # download data
    print('Downloading page ...')
    try:
        html_src = urlopen(url).read()
    except BadStatusLine:
        print('Exception: BadStatusLine')
        return False
    soup = BeautifulSoup(html_src)

    # parse page
    print('Parsing page ...')
    meta_keywords = soup.head.find('meta', attrs={'name': 'Keywords'})
    meta_description = soup.head.find('meta', attrs={'name': 'Description'})

    title = soup.title.string
    description = meta_description.attrs['content']
    keywords = meta_keywords.attrs['content']
    content = soup.get_text()

    # save data
    print('Saving data to database ...')
    domain = Domain.objects.create(name=domain_name, pagerank=0)
    domain.save()
    webpage = Webpage.objects.create(domain=domain,
                                     path=uri_path,
                                     title=title,
                                     description=description,
                                     keywords=keywords,
                                     content=content)
    webpage.save()

    # crawl rest of pages
    print('Delaying other pages to crawl and parse ...')
    urls = soup.find_all('a')
    for test_url in urls:
        url = test_url['href']
        if url[0] == '/':
            url = domain_name + url
        elif url.find('.') == -1:  # dot is allowed only in domain name
            url = domain_name + uri_path + ('/' if uri_path[-1] != '/' else '') + url
        if not url.startswith('http://'):
            url = 'http://' + url
        crawl_and_parse.delay(url)

    print('Done.')
    return True