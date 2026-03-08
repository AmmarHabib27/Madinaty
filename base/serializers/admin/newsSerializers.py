from rest_framework import serializers
from base.models import News


class NewsSerializer(serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            'id', 'title', 'body', 'image',
            'start_date', 'expiry_date', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'is_active', 'created_at']

    def get_is_active(self, obj):
        return obj.is_active


class NewsCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    body = serializers.CharField()
    image = serializers.ImageField(required=False, allow_null=True)
    start_date = serializers.DateTimeField()
    expiry_date = serializers.DateTimeField()

    def validate(self, attrs):
        if attrs['expiry_date'] <= attrs['start_date']:
            raise serializers.ValidationError({'expiry_date': 'Expiry date must be after start date.'})
        return attrs


class NewsUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=False)
    body = serializers.CharField(required=False)
    image = serializers.ImageField(required=False, allow_null=True)
    start_date = serializers.DateTimeField(required=False)
    expiry_date = serializers.DateTimeField(required=False)

    def validate(self, attrs):
        start = attrs.get('start_date')
        expiry = attrs.get('expiry_date')
        if start and expiry and expiry <= start:
            raise serializers.ValidationError({'expiry_date': 'Expiry date must be after start date.'})
        return attrs
