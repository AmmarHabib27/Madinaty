from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from base.models import User, UserRole


def _get_tokens(user) -> dict:
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def login_admin(email: str, password: str) -> tuple:
    """Authenticate admin with email and password, return (user, tokens)."""
    user = authenticate(username=email, password=password)
    if user is None or user.role != UserRole.ADMIN:
        raise AuthenticationFailed('Invalid credentials.')
    if not user.is_active:
        raise AuthenticationFailed('Account is disabled.')
    tokens = _get_tokens(user)
    return user, tokens


def change_password(user, old_password: str, new_password: str) -> None:
    if not user.check_password(old_password):
        raise AuthenticationFailed('Current password is incorrect.')
    user.set_password(new_password)
    user.save(update_fields=['password'])
