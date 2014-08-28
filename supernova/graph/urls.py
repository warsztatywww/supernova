from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns(
    '',
    url(r'^$', graph_view, name='graph'),
    url(r'^json$', graph_json, name='graph_json'),
)
