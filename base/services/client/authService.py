import random
from django.core.cache import cache
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed, ValidationError, NotFound
from rest_framework_simplejwt.tokens import RefreshToken
from base.models import User

OTP_TTL = 600  # 10 minutes
OTP_KEY_PREFIX = 'otp'
MOCK_OTP = '123456'


def _otp_cache_key(phone: str) -> str:
    return f'{OTP_KEY_PREFIX}:{phone}'


def _generate_otp() -> str:
    if getattr(settings, 'ENVIRONMENT', 'production') == 'staging':
        return MOCK_OTP
    return str(random.randint(10000, 99999))


def _send_sms(phone: str, otp: str) -> None:
    """Send OTP via SMS. In staging the OTP is always mocked — no SMS needed.
    In production, plug in your SMS gateway here (e.g. Twilio, Vonage)."""
    if getattr(settings, 'ENVIRONMENT', 'production') == 'staging':
        return
    if not phone:
        return
    # TODO: integrate SMS provider
    # Example (Twilio):
    # from twilio.rest import Client
    # Client(settings.TWILIO_SID, settings.TWILIO_TOKEN).messages.create(
    #     to=phone, from_=settings.TWILIO_FROM, body=f'Your Madinaty code: {otp}'
    # )


def _send_otp(user: User) -> None:
    otp = _generate_otp()
    cache.set(_otp_cache_key(user.phone), otp, timeout=OTP_TTL)
    _send_sms(user.phone, otp)


def _send_otp_to_phone(phone: str) -> None:
    """Lookup user by phone and send them an OTP."""
    try:
        user = User.objects.get(phone=phone)
    except User.DoesNotExist:
        raise NotFound('No account found with this phone number.')
    if not user.is_active:
        raise AuthenticationFailed('Account is disabled.')
    _send_otp(user)


def _get_tokens(user) -> dict:
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def register_user(validated_data: dict) -> None:
    """Create user account (unverified) and send OTP to phone."""
    User.objects.create_user(
        phone=validated_data['phone'],
        name=validated_data['name'],
        password=validated_data['password'],
    )
    _send_otp_to_phone(validated_data['phone'])


def login_user(phone: str, password: str) -> dict:
    """Authenticate with phone + password and return JWT tokens."""
    try:
        user = User.objects.get(phone=phone)
    except User.DoesNotExist:
        raise AuthenticationFailed('Invalid phone number or password.')

    if not user.check_password(password):
        raise AuthenticationFailed('Invalid phone number or password.')

    if not user.is_active:
        raise AuthenticationFailed('Account is disabled.')

    if not user.is_phone_verified:
        raise AuthenticationFailed('Please verify your phone number first.')

    return _get_tokens(user)


def resend_otp(phone: str) -> None:
    """Resend OTP to phone (usable for registration verification and forget password)."""
    _send_otp_to_phone(phone)


def verify_otp_and_login(phone: str, otp_code: str) -> tuple:
    """Verify OTP, mark phone as verified, and return (user, tokens)."""
    key = _otp_cache_key(phone)
    stored_otp = cache.get(key)

    if not stored_otp or stored_otp != otp_code:
        raise ValidationError({'otp': 'Invalid or expired verification code.'})

    cache.delete(key)

    try:
        user = User.objects.get(phone=phone)
    except User.DoesNotExist:
        raise NotFound('User not found.')

    if not user.is_phone_verified:
        user.is_phone_verified = True
        user.save(update_fields=['is_phone_verified'])

    return user, _get_tokens(user)


def send_forget_password_otp(phone: str) -> None:
    """Send OTP to phone for forget-password flow."""
    _send_otp_to_phone(phone)


def forget_password_confirm(phone: str, otp_code: str, new_password: str) -> None:
    """Verify OTP from forget-password flow and set a new password."""
    key = _otp_cache_key(phone)
    stored_otp = cache.get(key)

    if not stored_otp or stored_otp != otp_code:
        raise ValidationError({'otp': 'Invalid or expired verification code.'})

    cache.delete(key)

    try:
        user = User.objects.get(phone=phone)
    except User.DoesNotExist:
        raise NotFound('User not found.')

    user.set_password(new_password)
    user.save(update_fields=['password'])


def reset_password(user: User, old_password: str, new_password: str) -> None:
    """Change password for an authenticated user using their old password."""
    if not user.check_password(old_password):
        raise ValidationError({'old_password': 'Current password is incorrect.'})
    user.set_password(new_password)
    user.save(update_fields=['password'])


def get_user_by_id(user_id: int) -> User:
    try:
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise NotFound('User not found.')


def update_onesignal_player_id(user, player_id: str) -> None:
    user.onesignal_player_id = player_id
    user.save(update_fields=['onesignal_player_id'])
