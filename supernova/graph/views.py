from django.shortcuts import render_to_response
from supernova.websites.models import Domain, Webpage

def graph_view(request):
    return render_to_response(
        'graph.html',
        {},
    )