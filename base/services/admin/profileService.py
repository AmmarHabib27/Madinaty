from base.models import User, UserRole


def get_admin_profile(user) -> User:
    return user


def update_admin_profile(user, validated_data: dict) -> User:
    for attr, value in validated_data.items():
        setattr(user, attr, value)
    user.save()
    return user


def list_users():
    return User.objects.filter(role=UserRole.USER, is_active=True).order_by('-created_at')


def toggle_user_active(user_id: int) -> User:
    from rest_framework.exceptions import NotFound
    try:
        user = User.objects.get(id=user_id, role=UserRole.USER)
    except User.DoesNotExist:
        raise NotFound('User not found.')
    user.is_active = not user.is_active
    user.save(update_fields=['is_active'])
    return user
