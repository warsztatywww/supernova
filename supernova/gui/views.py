from django.http import Http404
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from accuracy.accuracy import accuracy

from bot.tasks import crawl_and_parse


def search_view(request):
    return render_to_response(
        'gui/search.html',
        {},
    )


def search_results_view(request, **kwargs):
    query = request.GET['query']
    webpages = accuracy(query) # returns a list of Webpage model objects
    results = []
    for i in webpages[:10]:
        results.append({
            'title': i.title,
            'description': i.description,
            'url': i.path
            })
    return render_to_response(
        'gui/search_results.html',
        {
            'query': query,
            'results': results
        },
    )


def submit_view(request):
    context = {
        'msg': None,
    }
    context.update(csrf(request))
    if 'submission' in request.POST:
        context['msg'] = 'Okay, we\'re indexing your site! Please be patient.'
        crawl_and_parse(request.POST['submission'])
    return render_to_response(
        'gui/submit.html',
        context,
    )
