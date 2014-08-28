from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns(
    '',
    url('^$', search_view, name='search'),
    url('^submit$', submit_view, name='submit'),
    url('^search$', search_results_view, name='search_results'),
)
