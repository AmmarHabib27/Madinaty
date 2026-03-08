from rest_framework.exceptions import AuthenticationFailed
from base.models import Admin
from base.tokens import AdminRefreshToken


def _get_tokens(admin) -> dict:
    refresh = AdminRefreshToken.for_admin(admin)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def login_admin(phone: str, password: str) -> tuple:
    """Authenticate admin with phone and password, return (admin, tokens)."""
    try:
        admin = Admin.objects.get(phone=phone)
    except Admin.DoesNotExist:
        raise AuthenticationFailed('Invalid credentials.')

    if not admin.check_password(password):
        raise AuthenticationFailed('Invalid credentials.')

    if not admin.is_active:
        raise AuthenticationFailed('Account is disabled.')

    tokens = _get_tokens(admin)
    return admin, tokens


def get_admin_by_id(admin_id: int) -> Admin:
    from rest_framework.exceptions import NotFound
    try:
        return Admin.objects.get(pk=admin_id)
    except Admin.DoesNotExist:
        raise NotFound('Admin not found.')


def change_password(admin, old_password: str, new_password: str) -> None:
    if not admin.check_password(old_password):
        raise AuthenticationFailed('Current password is incorrect.')
    admin.set_password(new_password)
    admin.save(update_fields=['password'])
