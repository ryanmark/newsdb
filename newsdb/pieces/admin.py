from django.contrib import admin
from . import models

import reversion


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
