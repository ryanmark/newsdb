from django.db import models
from django.utils.timezone import now
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

import reversion
from meta.models import ModelMeta
from sortedm2m.fields import SortedManyToManyField

from newsdb.models import SluggedModel

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


class Publication(SluggedModel):
    name = models.CharField(
        help_text="Name this product. May be publicly visible.",
        max_length=100)
    description = models.TextField(
        help_text="Extra description of this product. May "
        "be publicly visible.",
        blank=True)
    sites = models.ManyToManyField(Site)

    def __unicode__(self):
        return unicode(self.name)


class PublicationMeta(ModelMeta):
    publication = models.ForeignKey(Publication, related_name='meta')

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

    publications = models.ManyToManyField(
        Publication,
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
    type = models.CharField(max_length="16", default="story")
    status = models.CharField(
        help_text="Is this ready for public consumption?",
        max_length=16,
        default='draft', choices=STORY_STATUS_CHOICES)

    title = models.TextField(blank=True)
    brief = models.TextField(blank=True)

    publish_date = models.DateTimeField(default=now())
    update_date = models.DateTimeField(auto_now=True)

    publications = models.ManyToManyField(
        Publication,
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
        return reverse('story-detail', args=[self.slug])

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


STORY_ASSET_TYPE_CHOICES = (
    ('graf', 'Paragraph'),
    ('hed', 'Headline'),
    ('section_hed', 'Section headline'),
    ('embed', 'Embed'),
    ('img', 'Image'),
    ('data', 'Data'),
)


class StoryAsset(SluggedModel):
    type = models.CharField(max_length=16, choices=STORY_ASSET_TYPE_CHOICES)
    url = models.URLField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    story = SortedManyToManyField(Story)

    class Meta:
        verbose_name = "asset"
        verbose_name_plural = "assets"

reversion.register(StoryAsset)
