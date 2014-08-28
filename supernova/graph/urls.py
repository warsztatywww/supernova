from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns(
    '',
    url('^graph$', graph_view, name='graph'),
)
