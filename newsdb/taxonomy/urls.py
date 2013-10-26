from django.conf.urls import patterns, url, include
from rest_framework import viewsets, routers

from .models import Taxonomy, Term


# ViewSets define the view behavior.
class TaxonomyViewSet(viewsets.ModelViewSet):
    model = Taxonomy


class TermViewSet(viewsets.ModelViewSet):
    model = Term

# Routers provide an easy way of automatically determining the URL conf
#router = routers.DefaultRouter()
#router.register(r'terms', TermViewSet)
#router.register(r'', TaxonomyViewSet)

urlpatterns = patterns(
    '',
    url(r'^terms/?$', TermViewSet.as_view({'get': 'list'}), name="terms"),
    url(r'^terms/(?P<slug>[^/]+)$', TermViewSet.as_view({'get': 'retrieve'}),
        name="term_detail"),
    url(r'^$', TaxonomyViewSet.as_view({'get': 'list'}), name="taxonomies"),
    url(r'^(?P<slug>[^/]+)$', TaxonomyViewSet.as_view({'get': 'retrieve'}),
        name="taxonomy_detail")
    #url(r'^(?P<tax_slug>[^/]+)/terms/$', views.terms, name="terms"),
)
