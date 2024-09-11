from rest_framework import serializers
from pokemon.models import Pokemon, FileUpload
from taggit.serializers import TagListSerializerField, TaggitSerializer


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = 'file_url',


class PokemonSerializer(TaggitSerializer, serializers.ModelSerializer):
    type = TagListSerializerField()
    abilities = TagListSerializerField()
    egg_groups = TagListSerializerField()
    ev_yield = TagListSerializerField()
    files = FileUploadSerializer(many=True, source="fileupload_set")

    class Meta:
        model = Pokemon
        fields = ('id', 'created_at', 'updated_at', 'is_active', 'name', 'species', 'height', 'weight',
                  'growth_rate', 'abilities', 'type', 'egg_groups', 'ev_yield', 'files')
