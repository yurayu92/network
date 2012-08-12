from django.conf.urls import patterns, include, url
from django.conf import settings

from person.views import *


urlpatterns = patterns('',
    url(r'^$', login),
    url(r'^profile/(\d)+/$', person),
    url(r'^profile/update/$', person_update),
    url(r'^profile/friends/$', friends),
)

urlpatterns += patterns('',
    (r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True }),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT, 'show_indexes': True }),
)