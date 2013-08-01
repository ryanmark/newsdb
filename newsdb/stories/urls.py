from django.conf.urls import patterns, url
from . import api

urlpatterns = patterns('',
    url(r'^hello', api.hello),
    url(r'^stories/', api.stories)
)
