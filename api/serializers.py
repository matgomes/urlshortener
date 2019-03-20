from collections import OrderedDict

from rest_framework import serializers

from api.models import Url


class UrlSerializer(serializers.ModelSerializer):

    class Meta:
        model = Url
        fields = ['original_url', 'alias', 'hits']


class CustomSerializer(serializers.Serializer):

    def to_representation(self, instance):
        result = super(CustomSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ExceptionDetailSerializer(CustomSerializer):

    alias = serializers.CharField()
    err_code = serializers.CharField()
    description = serializers.CharField()


class UrlShortenResponseSerializer(CustomSerializer):

    original_url = serializers.CharField()
    url = serializers.CharField()
    alias = serializers.CharField()
    statistics = serializers.JSONField()
