from rest_framework import serializers
from base.models import Admin, User


class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'name', 'phone', 'profile_picture', 'created_at']
        read_only_fields = ['id', 'phone', 'created_at']


class AdminUpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['name', 'profile_picture']


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'phone', 'is_active', 'created_at']
