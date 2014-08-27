#import index
#import pagerank as pr
import 

result = {}
query = ''
query = query.split(' ')
for word in query:
    word = index.stem(word)
    indexedResult = index.get(word)
    for l in indexedResult:
        # correct assuming that l[0] is a Webpage model object and l[1] is a number of occurence of that word
        if l[0]['path'] in result:
            result[l[0]['path']]['number'] += l[1]
        else:
            result[l[0]['path']] = { 'webpage': l[0], 'number': l[1] }

for l in result:
    l.pagerank = pr.get(l.webpage.domain)

'''
Example for testing:
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
result = sorted(result.values(), key=lambda x: x['pagerank'] * x['number'], reverse=True)
return(i['webpage'] for i in result)
