from django.shortcuts import render_to_response
from django.http import HttpResponse
from supernova.websites.models import Domain, Webpage
import json

def graph_view(request):
    return render_to_response(
        'graph.html',
        {},
    )

def graph_json(request):
    data = {"nodes": [],
            "links": []}
    return HttpResponse(json.dumps(data), content_type="application/json")
