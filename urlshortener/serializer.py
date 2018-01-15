from rest_framework import serializers
from .models import urls

class shortenerSerializer(serializers.ModelSerializer):

    class Meta:
        model = urls
        depth = 1
        fields = ['original', 'alias', 'link', 'count']
