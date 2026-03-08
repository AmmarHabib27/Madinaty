from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings


class AdminRefreshToken(RefreshToken):
    """JWT refresh token for Admin model instances.

    Adds a 'user_type: admin' claim so that MultiModelJWTAuthentication
    can resolve the token against the admins table instead of the users table.
    """

    @classmethod
    def for_admin(cls, admin):
        token = cls()
        token[api_settings.USER_ID_CLAIM] = admin.pk
        token['user_type'] = 'admin'
        return token
