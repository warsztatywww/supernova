from django.http import Http404
from django.core.context_processors import csrf
from django.shortcuts import render_to_response

from bot.tasks import crawl_and_parse


def search_view(request):
    return render_to_response(
        'gui/search.html',
        {},
    )


def search_results_view(request, **kwargs):
    return render_to_response(
        'gui/search_results.html',
        {
            'query': request.GET['query'],
            'results': [
                {
                    'title': 'How To Get Rich In One Day?',
                    'description': 'Forex Bots With Neural Nets Deminary. This Week 30% Off! Have you ever imagined? '
                                   'For Deeper Discounts Name Your Own Price.',
                    'url': 'http://jaszczur.pl/',
                },
                {
                    'title': 'Pyszotok',
                    'description': 'Grigori Perelman, the Russian mathematician famous for solving '
                                   'the notorious Poincare conjecture, shocked the world of mathematics '
                                   'in 2006 by declining to accept the Fields Medal',
                    'url': 'http://pyszotok.wordpress.com/',
                },
                {
                    'title': 'Heroes of Might and Magic III / Heroes 3 - Age of Heroes',
                    'description': 'Heroes of Might and Magic III is a turn-based strategic war game, set up '
                                   'in a classical role-playing game Environment. It involves capturing and developing',
                    'url': 'http://www.heroesofmightandmagic.com/heroes3/heroesofmightandmagic3iii.shtml',
                },
            ],
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
