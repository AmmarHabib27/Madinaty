from rest_framework import serializers
from base.models import News


class NewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'body', 'image', 'expiry_at', 'created_at']


class NewsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'body', 'image', 'duration_hours', 'expiry_at', 'created_at']
