import re
from rest_framework import serializers
from base.models import User


def validate_password_strength(value):
    errors = []
    if len(value) < 8:
        errors.append('at least 8 characters')
    if not re.search(r'[A-Z]', value):
        errors.append('at least one uppercase letter')
    if not re.search(r'[a-z]', value):
        errors.append('at least one lowercase letter')
    if not re.search(r'\d', value):
        errors.append('at least one digit')
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=\[\]\\\/`~;']", value):
        errors.append('at least one special character')
    if errors:
        raise serializers.ValidationError(f'Password must contain: {", ".join(errors)}.')
    return value


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'phone', 'password']

    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError('An account with this phone number already exists.')
        return value

    def validate_password(self, value):
        return validate_password_strength(value)


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    password = serializers.CharField()


class ResendOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)


class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    otp = serializers.CharField(max_length=5, min_length=4)


class ForgetPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)


class ForgetPasswordConfirmSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    otp = serializers.CharField(max_length=5, min_length=4)
    new_password = serializers.CharField()

    def validate_new_password(self, value):
        return validate_password_strength(value)


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_new_password(self, value):
        return validate_password_strength(value)
