from django.http import Http404
from django.core.context_processors import csrf
from django.shortcuts import render_to_response


def search_view(request):
    return render_to_response(
        'gui/search.html',
        {},
    )


def search_results_view(request, **kwargs):
    return render_to_response(
        'gui/search_results.html',
        {
            'results': [],
        },
    )


def submit_view(request):
    return render_to_response(
        'gui/submit.html',
        {},
    )
