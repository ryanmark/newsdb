from django.contrib import admin
from newsdb.stories.models import Publication, PublicationMeta, Story, StoryMeta
from newsdb.stories.models import TermMeta, Taxonomy, Term

import reversion


class PublicationMetaInline(admin.TabularInline):
    model = PublicationMeta


class PublicationAdmin(admin.ModelAdmin):
    fields = ('name', 'slug', 'description')
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('slug', 'name')
    inlines = [
        PublicationMetaInline,
    ]
admin.site.register(Publication, PublicationAdmin)


class StoryMetaInline(admin.TabularInline):
    model = StoryMeta


class StoryAdmin(reversion.VersionAdmin):
    fields = ('title', 'slug', ('status', 'publish_date'),
              'brief', 'body', ('terms', 'publications'))
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('slug', 'title', 'status', 'publish_date')
    filter_horizontal = ('terms',)
    inlines = [
        StoryMetaInline,
    ]
admin.site.register(Story, StoryAdmin)


class TaxAdmin(admin.ModelAdmin):
    fields = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('slug', 'name')
admin.site.register(Taxonomy, TaxAdmin)


class TermMetaInline(admin.TabularInline):
    model = TermMeta


class TermAdmin(reversion.VersionAdmin):
    fields = ('name', 'slug', ('status', 'taxonomy'), 'brief',
              'body', 'publications')
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'slug', 'taxonomy')
    list_filter = ('taxonomy', 'status')
    inlines = [
        TermMetaInline,
    ]
admin.site.register(Term, TermAdmin)
