from rest_framework import serializers
from base.models import User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone', 'profile_picture', 'created_at']
        read_only_fields = ['id', 'email', 'created_at']


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'phone', 'profile_picture']
