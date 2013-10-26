from django.db import models
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

import reversion
from metamodel.models import ModelMeta
from sortedm2m.fields import SortedManyToManyField

from newsdb.models import SluggedModel

PIECE_TYPE_CHOICES = (
    ('story', 'Story'),
    ('embed', 'Embed'),
    ('img', 'Image'),
    ('data', 'Data'),
)

PIECE_STATUS_CHOICES = (
    ("draft",     "Draft"),
    ("submit",    "Ready for edit"),
    ("review",    "Needs review"),
    ("edited",    "Edited"),
    ("scheduled", "Scheduled"),
    ("published", "Published"),
)

TERM_STATUS_CHOICES = (
    ('published',  'Published'),
    ('draft', 'Draft'),
)


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
    status = models.CharField(
        help_text="Is this ready for public consumption?",
        max_length=16,
        default='draft', choices=TERM_STATUS_CHOICES)

    publications = models.ManyToManyField(
        Publication,
        related_name='terms',
        help_text="Where will this term be used?")

    def __unicode__(self):
        return unicode("%s (%s)" % (self.name, self.taxonomy))

    def get_slug_text(self):
        return unicode("%s" % self.name)

    class Meta:
        unique_together = ('taxonomy', 'slug')
        verbose_name_plural = 'terms'
reversion.register(Term, follow=["meta"])


class TermMeta(ModelMeta):
    term = models.ForeignKey(Term, related_name='meta')

    class Meta:
        unique_together = ('term', 'key')
        verbose_name = "term meta-data"
        verbose_name_plural = "term meta-data"
reversion.register(TermMeta)


class Piece(SluggedModel):
    type = models.CharField(
        help_text="What kind of piece is this?",
        max_length="16",
        default="story", choices=PIECE_TYPE_CHOICES)
    status = models.CharField(
        help_text="Is this ready for public consumption?",
        max_length=16,
        default='draft', choices=PIECE_STATUS_CHOICES)

    title = models.TextField(blank=True)
    brief = models.TextField(blank=True)
    body = models.TextField(blank=True)

    publish_date = models.DateTimeField(null=True)
    update_date = models.DateTimeField(auto_now=True)

    publications = models.ManyToManyField(
        Publication,
        related_name='stories',
        help_text="Who is this piece going to?")

    terms = models.ManyToManyField(
        Term,
        related_name='terms',
        help_text="Which terms should this story be associated with?")

    def __unicode__(self):
        return unicode(self.title)

    def get_absolute_url(self):
        return reverse('piece-detail', args=[self.slug])

    class Meta:
        unique_together = ('type', 'slug')
        verbose_name_plural = 'pieces'
reversion.register(Piece, follow=['meta'])


class PieceMeta(ModelMeta):
    piece = models.ForeignKey(Piece, related_name='meta')

    class Meta:
        unique_together = ('piece', 'key')
        verbose_name = "story meta-data"
        verbose_name_plural = "story meta-data"
reversion.register(PieceMeta)
