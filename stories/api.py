from tastypie.authentication import Authentication, BasicAuthentication, ApiKeyAuthentication, MultiAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ModelResource
from stories.models import Story, Product, StoryMeta, Taxonomy, Term
from tastypie import fields
from django.conf.urls import url
from tastypie.constants import ALL, ALL_WITH_RELATIONS


class TermResource(ModelResource):
    class Meta:
        queryset = Term.objects.all()
        resource_name = 'term'
        authorization = DjangoAuthorization()
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())


class StoryMetaResource(ModelResource):
    class Meta:
        queryset = StoryMeta.objects.all()
        resource_name = 'meta'
        fields = ['key', 'value']
        include_resource_uri = False
        authorization = DjangoAuthorization()
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())


class ProductResource(ModelResource):
    class Meta:
        queryset = Product.objects.all()
        resource_name = 'product'
        authorization = DjangoAuthorization()
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())


class StoryResource(ModelResource):
    terms = fields.ToManyField(TermResource, 'terms', full=True, blank=True)
    meta = fields.ToManyField(StoryMetaResource, 'meta', full=True, blank=True)
    #product = fields.ForeignKey(ProductResource, 'product', full=True, blank=True)

    class Meta:
        queryset = Story.objects.all()
        resource_name = 'story'
        authorization = DjangoAuthorization()
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        #detail_uri_name = 'slug'
        filtering = {
            "slug": ('exact', 'startswith',),
            "title": ALL,
            "terms": ALL_WITH_RELATIONS,
            "meta": ALL_WITH_RELATIONS,
            #"product": ALL_WITH_RELATIONS,
        }


class TaxonomyResource(ModelResource):
    class Meta:
        queryset = Taxonomy.objects.all()
        resource_name = 'taxonomy'
        authorization = DjangoAuthorization()
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())


