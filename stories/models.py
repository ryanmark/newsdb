from django.db import models
from django.utils.timezone import now
from django.template.defaultfilters import slugify
from django.contrib.sites.models import Site
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from newsapps.db.models import SluggedModel

STORY_STATUS_CHOICES = (
    ("published", "Published"),
    ("scheduled", "Scheduled"),
    ("draft",     "Draft"),
    ("submit",    "Ready for edit"),
    ("edited",    "Edited"),
    ("review",    "Needs review"),
)

STORY_TYPE_CHOICES = (
    ("story", "Story"),
)

TERM_STATUS_CHOICES = (
    ('published',  'Published'),
    ('draft', 'Draft'),
)


class ModelMeta(models.Model):
    key = models.SlugField()
    value = models.TextField()

    def __unicode__(self):
        return unicode(self.value)

    class Meta:
        abstract = True
        verbose_name = "item"


class Product(SluggedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return unicode(self.name)


class ProductMeta(ModelMeta):
    product = models.ForeignKey(Product, related_name='meta')

    class Meta:
        unique_together = ('product', 'key')
        verbose_name_plural = "product metadata"


class Taxonomy(SluggedModel):
    story_type = models.CharField(max_length=16, default='story')
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        unique_together = ('story_type', 'slug')
        verbose_name_plural = 'taxonomies'


class Term(SluggedModel):
    taxonomy = models.ForeignKey(Taxonomy, related_name='terms')

    name = models.CharField(max_length=200)
    brief = models.TextField(blank=True)
    body = models.TextField(blank=True)

    status = models.CharField(max_length=16,
            default='public', choices=TERM_STATUS_CHOICES)

    products = models.ManyToManyField(Product, related_name='terms')

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        unique_together = ('taxonomy', 'slug')
        verbose_name_plural = 'terms'


class TermMeta(ModelMeta):
    term = models.ForeignKey(Term, related_name='meta')

    class Meta:
        unique_together = ('term', 'key')
        verbose_name_plural = "term metadata"


class Story(SluggedModel):
    type = models.CharField(max_length=16, default='story')

    status = models.CharField(max_length=16,
            default='draft', choices=STORY_STATUS_CHOICES)

    title = models.TextField(blank=True)
    brief = models.TextField(blank=True)
    body = models.TextField(blank=True)
    publish_date = models.DateTimeField(default=now())

    trash = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)

    products = models.ManyToManyField(Product, related_name='stories')

    terms = models.ManyToManyField(Term, related_name='terms')

    def __unicode__(self):
        return unicode(self.title)

    def get_absolute_url(self):
        try:
            return unicode(self.meta.get(key='permalink'))
        except StoryMeta.DoesNotExist:
            return ""

    class Meta:
        unique_together = ('type', 'slug')
        verbose_name_plural = 'stories'


# Story post save signal
#@receiver(post_save, sender=Story)
#def story_post_save(sender, **kwargs):
    #instance = kwargs['instance']
    ## if the story doesn't have a site, add the current
    #if instance.sites.count() == 0:
        #instance.sites.add(Site.objects.get_current())


class StoryMeta(ModelMeta):
    story = models.ForeignKey(Story, related_name='meta')

    class Meta:
        unique_together = ('story', 'key')
        verbose_name_plural = "story metadata"


# Setup auto API key generation
from django.contrib.auth.models import User
from tastypie.models import create_api_key

models.signals.post_save.connect(create_api_key, sender=User)


class UserMeta(ModelMeta):
    user = models.ForeignKey(User, related_name='meta')

    class Meta:
        unique_together = ('user', 'key')
        verbose_name_plural = "user metadata"
