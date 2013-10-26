from django.db import models
from django.contrib.sites.models import Site

from newsdb.models import SluggedModel
from metamodel.models import ModelMeta


class Publication(SluggedModel):
    name = models.CharField(
        max_length=100)
    sites = models.ManyToManyField(Site)

    def __unicode__(self):
        return unicode(self.name)


class PublicationMeta(ModelMeta):
    publication = models.ForeignKey(Publication, related_name='meta')

    class Meta:
        verbose_name = "product meta-data"
        verbose_name_plural = "product meta-data"
