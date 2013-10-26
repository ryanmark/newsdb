from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^pieces/', include('newsdb.pieces.urls')),
    url(r'^taxonomy/', include('newsdb.taxonomy.urls')),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework'))
)
