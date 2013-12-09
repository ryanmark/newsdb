from django.db import models
from django.core.urlresolvers import reverse

from django_hstore import hstore

import reversion
#from sortedm2m.fields import SortedManyToManyField

from newsdb.models import SluggedModel, BodyField
from newsdb.publications.models import Publication
from newsdb.taxonomy.models import Term

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
    text = models.TextField(blank=True)
    body = BodyField()

    data = hstore.DictionaryField(db_index=True)
    objects = hstore.HStoreManager()

    publish_date = models.DateTimeField(null=True)
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

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
