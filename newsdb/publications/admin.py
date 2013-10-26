from django.contrib import admin
from . import models


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
