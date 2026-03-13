from rest_framework import serializers
from base.models import User


class ProfileSerializer(serializers.ModelSerializer):
    total_complaints = serializers.SerializerMethodField()
    resolved_complaints = serializers.SerializerMethodField()
    points = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'phone', 'profile_picture', 'created_at',
                  'total_complaints', 'resolved_complaints', 'points']
        read_only_fields = ['id', 'phone', 'created_at']

    def get_total_complaints(self, obj):
        return obj.complaints.count()

    def get_resolved_complaints(self, obj):
        return obj.complaints.filter(status='resolved').count()

    def get_points(self, obj):
        return obj.complaints.filter(status='resolved').count() * 10


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'profile_picture', 'phone']

    def validate_phone(self, value):
        qs = User.objects.filter(phone=value).exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('This phone number is already in use.')
        return value
