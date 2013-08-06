from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^hello', views.hello),
    url(r'^stories/', views.stories, name="stories"),
    url(r'^stories/(?P<slug>[^/]+)$', views.story_detail, name="story-detail")
)
