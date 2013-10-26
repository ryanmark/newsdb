from rest_framework import serializers
from .models import Taxonomy


class TaxonomySerializer(serializers.ModelSerializer):
    exclude_fields = ('id',)

    class Meta:
        model = Taxonomy
        lookup_field = 'slug'
