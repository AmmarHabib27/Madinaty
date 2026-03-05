from rest_framework import serializers
from base.models import News


class NewsSerializer(serializers.ModelSerializer):
    is_expired = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            'id', 'title', 'body', 'image', 'is_active',
            'duration_hours', 'expiry_at', 'is_expired', 'created_at'
        ]
        read_only_fields = ['id', 'expiry_at', 'is_expired', 'created_at']

    def get_is_expired(self, obj):
        return obj.is_expired


class NewsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['title', 'body', 'image', 'is_active', 'duration_hours']


class NewsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['title', 'body', 'image', 'is_active', 'duration_hours']
