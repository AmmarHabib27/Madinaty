import random
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed, ValidationError, NotFound
from rest_framework_simplejwt.tokens import RefreshToken
from base.models import User, UserRole

OTP_TTL = 600  # 10 minutes
OTP_KEY_PREFIX = 'otp'


def _otp_cache_key(email: str) -> str:
    return f'{OTP_KEY_PREFIX}:{email}'


def _generate_otp() -> str:
    return str(random.randint(100000, 999999))


def _get_tokens(user) -> dict:
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def register_user(validated_data: dict) -> None:
    """Create user account and send OTP in one step."""
    user = User.objects.create_user(
        email=validated_data['email'],
        name=validated_data['name'],
        phone=validated_data.get('phone', ''),
    )
    _send_otp(user.email)


def request_otp(email: str) -> None:
    """Send OTP to an existing user's email."""
    try:
        user = User.objects.get(email=email, role=UserRole.USER)
    except User.DoesNotExist:
        raise NotFound('No account found with this email.')

    if not user.is_active:
        raise AuthenticationFailed('Account is disabled.')

    _send_otp(email)


def _send_otp(email: str) -> None:
    otp = _generate_otp()
    cache.set(_otp_cache_key(email), otp, timeout=OTP_TTL)
    send_mail(
        subject='Madinaty - Your Login Code',
        message=f'Your verification code is: {otp}\nThis code expires in 10 minutes.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )


def verify_otp_and_login(email: str, otp_code: str) -> tuple:
    """Verify OTP from Redis, return (user, tokens) on success."""
    key = _otp_cache_key(email)
    stored_otp = cache.get(key)

    if not stored_otp or stored_otp != otp_code:
        raise ValidationError({'otp': 'Invalid or expired verification code.'})

    cache.delete(key)

    try:
        user = User.objects.get(email=email, role=UserRole.USER)
    except User.DoesNotExist:
        raise NotFound('User not found.')

    tokens = _get_tokens(user)
    return user, tokens


def update_onesignal_player_id(user, player_id: str) -> None:
    user.onesignal_player_id = player_id
    user.save(update_fields=['onesignal_player_id'])
