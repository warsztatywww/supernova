import index
import nltk
import re
import string

stemmer = nltk.stem.snowball.EnglishStemmer()
keywordRate = 0.3
titleRate = 2

def stringToList(a, splitString):
    '''
    :param a: string to process
    :param splitString: string at which `a` should be splitted

    :return: list of stemmed words from `a`
    '''
    a = "".join(l for l in a if l not in string.punctuation).split(splitCharacter)
    return [stemmer.stem(i) for i in a if i != '']

def calculatePoints(query, stringToCheck, splitString, rate):
    '''
    :param query: list of stemmed words from user's query
    :param stringToCheck: string for which we should check if words from `query` are there
    :param splitString: string at which `stringToCheck` should be splitter
    :param rate: rate which we add for every word from `query` in `stringToCheck`

    :return: return number of points
    '''
    result = 1
    stringToCheck = stringToList(stringToCheck, splitString)
    for word in query:
        if word in stringToCheck:
            result += rate
    return result

def accuracy(query):
    '''
    The only function supposed to be used from outside. Responsible for getting Webpage model objects for a certain query and
    sorts it properly.

    :param query: user's query string

    :return: sorted list of Webpage model objects


    Example data for testing sorting:
    class Webpage(object):
        def __init__(self, domain, path):
            self.domain = domain
            self.path = path


    result = {
        'https://docs.python.org/3.4/library/functions.html#sorted': { 'webpage': Webpage('docs.python.org', 'https://docs.python.org/3.4/library/functions.html#sorted'), 'number': 15, 'pagerank': 2 },
        'http://www.wikiwand.com/en/Search_engine_(computing)': { 'webpage': Webpage('wikiwand.com', 'http://www.wikiwand.com/en/Search_engine_(computing)'), 'number': 10, 'pagerank': 3.5},
        'https://github.com/pathes/supernova': { 'webpage': Webpage('github.com', 'https://github.com/pathes/supernova'), 'number': 28, 'pagerank': 1 },
        'http://text-processing.com': { 'webpage': Webpage('text-processing.com', 'http://text-processing.com'), 'number': 10, 'pagerank': 2 }
    }
    '''
    query = stringToList(query, ' ')
    result = {}
    for word in query:
        indexedResult = index.get(word)
        for l in indexedResult:
            # correct assuming that l[0] is a Webpage model object and l[1] is a number of occurence of that word
            if l[0].path in result:
                result[ l[0].path ]['number'] += l[1]
            else:
                result[ l[0].path ] = { 'webpage': l[0], 'number': l[1] }

    for l in result:
        l['pagerank'] = l.webpage.domain.pagerank
        l['titlePoints'] = calculatePoints(query, l.webpage.title, ' ', titleRate)
        l['keywordPoints'] = calculatePoints(query, l.webpage.keywords, ',', keywordRate)


    compare = lambda x: x['pagerank'] * x['number'] * x['titlePoints'] * x['keywordPoints']
    result = sorted(result.values(), key=compare, reverse=True)
    return(i['webpage'] for i in result)
