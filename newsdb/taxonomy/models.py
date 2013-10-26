from django.db import models

import reversion
from newsdb.models import SluggedModel
from metamodel.models import ModelMeta

from newsdb.publications.models import Publication

TERM_STATUS_CHOICES = (
    ('published',  'Published'),
    ('draft', 'Draft'),
)


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
