from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^graph/', include('graph.urls')),
    url(r'^', include('gui.urls')),
)
