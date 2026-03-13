from rest_framework import serializers
from base.models import Complaint, ComplaintMedia


class ComplaintMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintMedia
        fields = ['id', 'file', 'media_type', 'uploaded_at']


class ComplaintCreateSerializer(serializers.ModelSerializer):
    media_files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Complaint
        fields = [
            'title', 'description', 'category', 'date',
            'latitude', 'longitude', 'location_address', 'media_files'
        ]

    def validate_category(self, value):
        if not value.is_active:
            raise serializers.ValidationError('Selected category is not active.')
        return value

    def create(self, validated_data):
        media_files = validated_data.pop('media_files', [])
        complaint = Complaint.objects.create(**validated_data)
        for file in media_files:
            media_type = 'video' if file.content_type.startswith('video') else 'image'
            ComplaintMedia.objects.create(complaint=complaint, file=file, media_type=media_type)
        return complaint


class ComplaintListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    media = ComplaintMediaSerializer(many=True, read_only=True)

    class Meta:
        model = Complaint
        fields = [
            'id', 'title', 'description', 'category', 'category_name',
            'status', 'priority', 'admin_comment', 'date',
            'latitude', 'longitude', 'location_address',
            'media', 'created_at', 'updated_at'
        ]


class ComplaintDetailSerializer(ComplaintListSerializer):
    pass
