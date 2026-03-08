from rest_framework import serializers
from base.models import User


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)


class ResendOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)


class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    otp = serializers.CharField(max_length=6, min_length=4)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'phone']

    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError('An account with this phone number already exists.')
        return value
