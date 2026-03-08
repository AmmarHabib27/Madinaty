from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.exceptions import ValidationError

from base.permissions import IsAdminUser
from base.serializers.admin import AdminLoginSerializer, AdminChangePasswordSerializer
from base.services.admin import authService
from base.utils import api_response


class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        admin, tokens = authService.login_admin(
            serializer.validated_data['phone'],
            serializer.validated_data['password'],
        )
        return api_response('Logged in successfully.', data=tokens)


class AdminTokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh', '').strip()
        if not refresh_token:
            raise ValidationError({'refresh': 'This field is required.'})
        try:
            token = RefreshToken(refresh_token)
            if token.get('user_type') != 'admin':
                raise ValidationError({'refresh': 'Invalid token.'})
            token.blacklist()
            admin = authService.get_admin_by_id(token['user_id'])
            from base.tokens import AdminRefreshToken
            new_refresh = AdminRefreshToken.for_admin(admin)
            return api_response('Token refreshed.', data={
                'refresh': str(new_refresh),
                'access': str(new_refresh.access_token),
            })
        except TokenError as e:
            raise InvalidToken({'refresh': str(e)})


class AdminLogoutView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        refresh_token = request.data.get('refresh', '').strip()
        if not refresh_token:
            raise ValidationError({'refresh': 'This field is required.'})
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError as e:
            raise ValidationError({'refresh': 'Invalid or already used refresh token.'}) from e
        return api_response('Logged out successfully.')


class AdminChangePasswordView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = AdminChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        authService.change_password(
            request.user,
            serializer.validated_data['old_password'],
            serializer.validated_data['new_password'],
        )
        return api_response('Password changed successfully.')
