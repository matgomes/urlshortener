from rest_framework import serializers

from api.models import Url


class UrlSerializer(serializers.ModelSerializer):

    class Meta:
        model = Url
        fields = ['original_url', 'alias', 'hits']
