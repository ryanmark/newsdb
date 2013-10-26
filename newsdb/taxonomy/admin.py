from django.contrib import admin
from . import models

import reversion


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
