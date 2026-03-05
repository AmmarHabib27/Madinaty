from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from base.serializers.client import (
    RegisterSerializer,
    RequestOTPSerializer,
    VerifyOTPSerializer,
)
from base.services.client import authService


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        authService.register_user(serializer.validated_data)
        return Response(
            {'detail': 'Account created. Verification code sent to your email.'},
            status=status.HTTP_201_CREATED,
        )


class RequestOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        authService.request_otp(serializer.validated_data['email'])
        return Response({'detail': 'Verification code sent to your email.'})


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, tokens = authService.verify_otp_and_login(
            serializer.validated_data['email'],
            serializer.validated_data['otp'],
        )
        return Response({
            'refresh': tokens['refresh'],
            'access': tokens['access'],
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass
        return Response({'detail': 'Logged out successfully.'})


class UpdateOneSignalPlayerIdView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        player_id = request.data.get('player_id', '').strip()
        if not player_id:
            return Response({'detail': 'player_id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        authService.update_onesignal_player_id(request.user, player_id)
        return Response({'detail': 'Player ID updated.'})
