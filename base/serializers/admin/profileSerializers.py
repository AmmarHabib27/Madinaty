from rest_framework import serializers
from base.models import User


class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone', 'profile_picture', 'role', 'created_at']
        read_only_fields = ['id', 'email', 'role', 'created_at']


class AdminUpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'phone', 'profile_picture']


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone', 'role', 'is_active', 'created_at']
