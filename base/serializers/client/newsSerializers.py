from rest_framework import serializers
from base.models import News


class NewsListSerializer(serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ['id', 'title', 'body', 'image', 'start_date', 'expiry_date', 'is_active', 'created_at']

    def get_is_active(self, obj):
        return obj.is_active


class NewsDetailSerializer(serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ['id', 'title', 'body', 'image', 'start_date', 'expiry_date', 'is_active', 'created_at']

    def get_is_active(self, obj):
        return obj.is_active
