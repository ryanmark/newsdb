from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^hello', views.hello),
    url(r'^pieces/', views.pieces, name="pieces"),
    url(r'^pieces/(?P<slug>[^/]+)$', views.piece_detail, name="piece-detail")
)
