from rest_framework import serializers
from .models import Piece


class ModelMetaSerializer(serializers.ModelSerializer):
    exclude_fields = ('id', 'meta')
    _model_meta = None

    def __init__(self, *args, **kwargs):

        # Instatiate the superclass normally
        super(ModelMetaSerializer, self).__init__(*args, **kwargs)

        # Drop internally used fields.
        for field_name in self.exclude_fields:
            if field_name in self.fields:
                self.fields.pop(field_name)

        print(type(self.data))
        print(type(self.object))

    def restore_object(self, attrs, instance=None):
        """
        restore a model instance
        """
        field_data, self._model_meta = self.split_fields(attrs)

        # Create new instance
        instance = super(ModelMetaSerializer, self
                         ).restore_object(field_data, instance)

        return instance

    def split_fields(self, data):
        """
        Takes a dictionary of data and a list of valid fields, returns two
        dictionaries, one with the corresponding fields from the data, and one
        with the leftovers
        """
        field_data = dict()
        meta_data = dict()
        for k, v in data.iteritems():
            if k in self.exclude_fields:
                continue
            elif k in self.fields.keys():
                field_data[k] = v
            else:
                meta_data[k] = v

        return field_data, meta_data


class PieceSerializer(serializers.ModelSerializer):
    exclude_fields = ('id',)

    class Meta:
        model = Piece
        lookup_field = 'slug'
