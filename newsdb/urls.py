from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from stories.api import StoryResource, ProductResource, TaxonomyResource, TermResource
from tastypie.api import Api

from django.contrib import admin

v1_api = Api(api_name='v1')
v1_api.register(StoryResource())
v1_api.register(ProductResource())
v1_api.register(TaxonomyResource())
v1_api.register(TermResource())

admin.autodiscover()

urlpatterns = patterns('',
    (r'^api/', include(v1_api.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

