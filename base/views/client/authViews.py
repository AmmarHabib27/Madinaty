import uuid

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.exceptions import ValidationError

from base.permissions import IsRegularUser
from base.serializers.client import (
    RegisterSerializer,
    LoginSerializer,
    ResendOTPSerializer,
    VerifyOTPSerializer,
    ForgetPasswordSerializer,
    ResetPasswordSerializer,
)
from base.services.client import authService
from base.utils import api_response


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        authService.register_user(serializer.validated_data)
        return api_response('Account created. Verification code sent to your phone.', http_status=201)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = authService.login_user(
            serializer.validated_data['phone'],
            serializer.validated_data['password'],
        )
        return api_response('Logged in successfully.', data=tokens)


class ResendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        authService.resend_otp(serializer.validated_data['phone'])
        return api_response('Verification code resent to your phone.')


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, tokens = authService.verify_otp_and_login(
            serializer.validated_data['phone'],
            serializer.validated_data['otp'],
        )
        return api_response('Phone verified. Logged in successfully.', data=tokens)


class ForgetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        authService.send_forget_password_otp(serializer.validated_data['phone'])
        return api_response('Verification code sent to your phone.')


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        authService.reset_password(
            serializer.validated_data['phone'],
            serializer.validated_data['otp'],
            serializer.validated_data['new_password'],
        )
        return api_response('Password reset successfully.')


class TokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh', '').strip()
        if not refresh_token:
            raise ValidationError({'refresh': 'This field is required.'})
        try:
            token = RefreshToken(refresh_token)
            if token.get('user_type') == 'admin':
                raise ValidationError({'refresh': 'Invalid token.'})
            token.blacklist()
            new_refresh = RefreshToken.for_user(
                authService.get_user_by_id(token['user_id'])
            )
            return api_response('Token refreshed.', data={
                'refresh': str(new_refresh),
                'access': str(new_refresh.access_token),
            })
        except TokenError as e:
            raise InvalidToken({'refresh': str(e)})


class LogoutView(APIView):
    permission_classes = [IsRegularUser]

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


class UpdateOneSignalPlayerIdView(APIView):
    permission_classes = [IsRegularUser]

    def post(self, request):
        player_id = request.data.get('player_id', '').strip()
        if not player_id:
            raise ValidationError({'player_id': 'This field is required.'})
        try:
            uuid.UUID(player_id)
        except ValueError:
            raise ValidationError({'player_id': 'Must be a valid UUID.'})
        authService.update_onesignal_player_id(request.user, player_id)
        return api_response('Player ID updated.')
