from rest_framework.exceptions import ValidationError
from base.models import User


def get_profile(user) -> User:
    return user


def update_profile(user, validated_data: dict) -> User:
    for attr, value in validated_data.items():
        setattr(user, attr, value)
    user.save()
    return user


def delete_profile_picture(user) -> None:
    if not user.profile_picture:
        raise ValidationError({'profile_picture': 'No profile picture to delete.'})
    user.profile_picture.delete(save=False)
    user.profile_picture = None
    user.save(update_fields=['profile_picture'])
