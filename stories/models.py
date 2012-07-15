from django.db import models
from django.utils.timezone import now
from django.template.defaultfilters import slugify
from django.contrib.sites.models import Site
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

import reversion

from newsapps.db.models import SluggedModel

STORY_STATUS_CHOICES = (
    ("draft",     "Draft"),
    ("submit",    "Ready for edit"),
    ("review",    "Needs review"),
    ("edited",    "Edited"),
    ("scheduled", "Scheduled"),
    ("published", "Published"),
)

STORY_TYPE_CHOICES = (
    ("story", "Story"),
)

TERM_STATUS_CHOICES = (
    ('published',  'Published'),
    ('draft', 'Draft'),
)


class ModelMeta(models.Model):
    """
    Abstract model for creating a meta-data model. Meta-data are totally
    arbitrary bits of text or code that describes the model in some way.
    """
    key = models.SlugField(
            help_text="The ID name of this bit of data. Should be only "
            "lowercase numbers and letters, dashes or underscores. No spaces.")
    value = models.TextField(
            help_text="The value, data or code for this item")

    def __unicode__(self):
        return unicode(self.value)

    class Meta:
        abstract = True


class Product(SluggedModel):
    name = models.CharField(
            help_text="Name this product. May be publicly visible.",
            max_length=100)
    description = models.TextField(
            help_text="Extra description of this product. May "
            "be publicly visible.",
            blank=True)

    def __unicode__(self):
        return unicode(self.name)


class ProductMeta(ModelMeta):
    product = models.ForeignKey(Product, related_name='meta')

    class Meta:
        verbose_name = "product meta-data"
        verbose_name_plural = "product meta-data"


class Taxonomy(SluggedModel):
    name = models.CharField(
        help_text="The name of this system of organization. "
        "Keep the name simple, like \"Category,\" \"Person\" or \"Issue.\"",
        max_length=100)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name_plural = 'taxonomies'


class Term(SluggedModel):
    taxonomy = models.ForeignKey(Taxonomy, related_name='terms')

    name = models.CharField(
            help_text="Name of this term or topic that falls under the chosen "
            "taxonomy or system of organization. This will appear to "
            "the public, so write something nice, like \"Bugs Bunny,\" "
            "\"Fire retardants\" or \"Elections 2012.\"",
            max_length=200)
    brief = models.TextField(
            help_text="A brief abstract or description. An elevator pitch."
            "The \"tweet\" for this package of stories.",
            blank=True)
    body = models.TextField(
            help_text="Introduce this topic, issue, person.", blank=True)

    status = models.CharField(
            help_text="Is this term or topic ready for public consumption? "
            "This has no effect on the published status of stories.",
            max_length=16,
            default='public', choices=TERM_STATUS_CHOICES)

    products = models.ManyToManyField(Product,
            related_name='terms',
            help_text="Who is this piece going to?")

    def __unicode__(self):
        return unicode("%s (%s)" % (self.name, self.taxonomy))

    def get_slug_text(self):
        return unicode("%s" % self.name)

    class Meta:
        unique_together = ('taxonomy', 'slug')
        verbose_name_plural = 'terms'


class TermMeta(ModelMeta):
    term = models.ForeignKey(Term, related_name='meta')

    class Meta:
        unique_together = ('term', 'key')
        verbose_name = "term meta-data"
        verbose_name_plural = "term meta-data"

reversion.register(Term, follow=["meta"])
reversion.register(TermMeta)


class Story(SluggedModel):
    type = models.CharField(
            help_text="Not sure what this is for yet...",
            max_length=16, default='story')

    status = models.CharField(
            help_text="Is this ready for public consumption?",
            max_length=16,
            default='draft', choices=STORY_STATUS_CHOICES)

    title = models.TextField(blank=True)
    brief = models.TextField(blank=True)
    body = models.TextField(blank=True)

    publish_date = models.DateTimeField(default=now())
    update_date = models.DateTimeField(auto_now=True)

    products = models.ManyToManyField(
            Product,
            related_name='stories',
            help_text="Who is this piece going to?")

    terms = models.ManyToManyField(
            Term,
            related_name='terms',
            help_text="Which terms or topics should this story be "
            "associated with?")

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


class StoryMeta(ModelMeta):
    story = models.ForeignKey(Story, related_name='meta')

    class Meta:
        unique_together = ('story', 'key')
        verbose_name = "story meta-data"
        verbose_name_plural = "story meta-data"

reversion.register(Story, follow=['meta'])
reversion.register(StoryMeta)


# Setup auto API key generation
from django.contrib.auth.models import User
from tastypie.models import create_api_key

models.signals.post_save.connect(create_api_key, sender=User)


class UserMeta(ModelMeta):
    user = models.ForeignKey(User, related_name='meta')

    class Meta:
        unique_together = ('user', 'key')
        verbose_name_plural = "user metadata"
