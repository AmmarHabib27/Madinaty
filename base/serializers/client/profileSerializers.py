from rest_framework import serializers
from base.models import User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'phone', 'profile_picture', 'created_at']
        read_only_fields = ['id', 'phone', 'created_at']


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'profile_picture']
