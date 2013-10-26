from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.pieces, name="pieces"),
    url(r'^(?P<slug>[^/]+)$', views.piece_detail, name="piece-detail")
)
