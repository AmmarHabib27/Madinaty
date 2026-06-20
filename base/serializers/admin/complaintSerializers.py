from rest_framework import serializers
from base.models import Complaint, ComplaintMedia, ComplaintStatus, ComplaintPriority


class ComplaintMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintMedia
        fields = ['id', 'file', 'media_type', 'uploaded_at']


class AdminComplaintListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_phone = serializers.CharField(source='user.phone', read_only=True)

    class Meta:
        model = Complaint
        fields = [
            'id', 'title', 'description', 'category', 'category_name',
            'user', 'user_name', 'user_phone',
            'status', 'priority', 'admin_comment',
            'latitude', 'longitude', 'location_address',
            'created_at', 'updated_at'
        ]


class AdminComplaintDetailSerializer(AdminComplaintListSerializer):
    media = ComplaintMediaSerializer(many=True, read_only=True)

    class Meta(AdminComplaintListSerializer.Meta):
        fields = AdminComplaintListSerializer.Meta.fields + ['media']


class AdminComplaintMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ['id', 'latitude', 'longitude', 'location_address', 'priority']


class UpdateComplaintStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=ComplaintStatus.choices)
    priority = serializers.ChoiceField(choices=ComplaintPriority.choices, required=False)
    admin_comment = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        if attrs['status'] in [ComplaintStatus.REJECTED, ComplaintStatus.ON_HOLD]:
            if not attrs.get('admin_comment', '').strip():
                raise serializers.ValidationError(
                    {'admin_comment': 'A comment is required when rejecting or placing on hold.'}
                )
        return attrs
