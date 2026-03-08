from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken
from rest_framework_simplejwt.settings import api_settings


class MultiModelJWTAuthentication(JWTAuthentication):
    """JWT authentication that resolves tokens for both User and Admin models.

    Admin tokens carry a 'user_type: admin' claim (set by AdminRefreshToken).
    All other tokens are resolved against the standard AUTH_USER_MODEL (User).
    """

    def get_user(self, validated_token):
        if validated_token.get('user_type') == 'admin':
            return self._get_admin(validated_token)
        return super().get_user(validated_token)

    def _get_admin(self, validated_token):
        from base.models import Admin

        try:
            admin_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken('Token contained no recognizable user identification.')

        try:
            admin = Admin.objects.get(pk=admin_id)
        except Admin.DoesNotExist:
            raise AuthenticationFailed('Admin not found.', code='user_not_found')

        if not admin.is_active:
            raise AuthenticationFailed('Admin account is disabled.')

        return admin
