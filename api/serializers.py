from rest_framework import serializers

from api.models import Url


class UrlSerializer(serializers.ModelSerializer):

    class Meta:
        model = Url
        fields = ['original_url', 'alias', 'hits']


class CustomSerializer(serializers.Serializer):

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
