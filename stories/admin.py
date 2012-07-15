from django.contrib import admin
from stories.models import *

import reversion


class ProductMetaInline(admin.TabularInline):
    model = ProductMeta


class ProductAdmin(admin.ModelAdmin):
    fields = ('name', 'slug', 'description')
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('slug', 'name')
    inlines = [
        ProductMetaInline,
    ]
admin.site.register(Product, ProductAdmin)


class StoryMetaInline(admin.TabularInline):
    model = StoryMeta


class StoryAdmin(reversion.VersionAdmin):
    fields = ('title', 'slug', ('status', 'publish_date'),
        'brief', 'body', ('terms', 'products'))
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
            'body', 'products')
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'slug', 'taxonomy')
    list_filter = ('taxonomy', 'status')
    inlines = [
        TermMetaInline,
    ]
admin.site.register(Term, TermAdmin)
