from django.contrib import admin
from . import models

import reversion


class PublicationMetaInline(admin.TabularInline):
    model = models.PublicationMeta


class PublicationAdmin(admin.ModelAdmin):
    fields = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('slug', 'name')
    inlines = [
        PublicationMetaInline,
    ]
admin.site.register(models.Publication, PublicationAdmin)


class PieceMetaInline(admin.TabularInline):
    model = models.PieceMeta


class PieceAdmin(reversion.VersionAdmin):
    fields = ('title', 'slug', ('status', 'publish_date'),
              'brief', 'body', ('terms', 'publications'))
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('slug', 'title', 'status', 'publish_date')
    filter_horizontal = ('terms',)
    inlines = [
        PieceMetaInline,
    ]
admin.site.register(models.Piece, PieceAdmin)


class TaxAdmin(admin.ModelAdmin):
    fields = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('slug', 'name')
admin.site.register(models.Taxonomy, TaxAdmin)


class TermMetaInline(admin.TabularInline):
    model = models.TermMeta


class TermAdmin(reversion.VersionAdmin):
    fields = ('name', 'slug', ('status', 'taxonomy'), 'publications')
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'slug', 'taxonomy')
    list_filter = ('taxonomy', 'status')
    inlines = [
        TermMetaInline,
    ]
admin.site.register(models.Term, TermAdmin)
