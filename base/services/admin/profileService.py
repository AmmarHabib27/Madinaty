from base.models import Admin, User


def get_admin_profile(admin) -> Admin:
    return admin


def update_admin_profile(admin, validated_data: dict) -> Admin:
    for attr, value in validated_data.items():
        setattr(admin, attr, value)
    admin.save()
    return admin


def list_users():
    return User.objects.filter(is_active=True).order_by('-created_at')


def toggle_user_active(user_id: int) -> User:
    from rest_framework.exceptions import NotFound
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise NotFound('User not found.')
    user.is_active = not user.is_active
    user.save(update_fields=['is_active'])
    return user
