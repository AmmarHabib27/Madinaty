from rest_framework.exceptions import ValidationError
from base.models import User
from base.services.client.authService import _send_otp_to_phone


def get_profile(user) -> User:
    return user


def update_profile(user, validated_data: dict) -> User:
    phone_changed = 'phone' in validated_data and validated_data['phone'] != user.phone
    for attr, value in validated_data.items():
        setattr(user, attr, value)
    if phone_changed:
        user.is_phone_verified = False
    user.save()
    if phone_changed:
        _send_otp_to_phone(user.phone)
    return user


def delete_profile_picture(user) -> None:
    if not user.profile_picture:
        raise ValidationError({'profile_picture': 'No profile picture to delete.'})
    user.profile_picture.delete(save=False)
    user.profile_picture = None
    user.save(update_fields=['profile_picture'])
