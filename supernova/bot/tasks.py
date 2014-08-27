from __future__ import absolute_import


from bot.celery import app

# TODO delete these useless methods
@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)


# TODO must be finished by mrowqa
@app.task
def crawl_and_parse(url):
    # TODO check whether page parsed in last 1h

    url_parsed = re.match('^(?:https?://)?(?P<domain>[a-z0-9\.]+)(?P<uri>.+)?$')
    domain_name = url_parsed.group('domain').lower()
    try:
        uri_path = url_parsed.group('uri')
    except IndexError:
        uri_path = '/'


    # download data
    try:
        html_src = urlopen(url).read()
    except BadStatusLine:
        return False
    soup = BeautifulSoup(html_src)

    # parse page
    meta_keywords = soup.head.find('meta', attrs={'name': 'Keywords'})
    meta_description = soup.head.find('meta', attrs={'name': 'Description'})

    title = soup.title.string
    description = meta_description.attrs['content']
    keywords = meta_keywords.attrs['content']
    content = soup.get_text()

    # save data
    domain = Domain.objects.create(name=domain_name)
    domain.save()
    webpage = Webpage.objects.create(domain=domain,
                                     path=uri_path,
                                     title=title,
                                     description=description,
                                     keywords=keywords,
                                     content=content)
    webpage.save()

    # crawl rest of pages



    return True