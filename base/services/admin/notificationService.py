import requests
from django.conf import settings


ONESIGNAL_API_URL = 'https://onesignal.com/api/v1/notifications'


def _build_headers() -> dict:
    return {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {settings.ONESIGNAL_REST_API_KEY}',
    }


def send_to_all(title: str, message: str, data: dict = None) -> dict:
    """Send push notification to all subscribed users."""
    payload = {
        'app_id': settings.ONESIGNAL_APP_ID,
        'included_segments': ['All'],
        'headings': {'en': title},
        'contents': {'en': message},
    }
    if data:
        payload['data'] = data
    return _post(payload)


def send_to_user(player_id: str, title: str, message: str, data: dict = None) -> dict:
    """Send push notification to a specific user by their OneSignal player ID."""
    if not player_id:
        return {}
    payload = {
        'app_id': settings.ONESIGNAL_APP_ID,
        'include_player_ids': [player_id],
        'headings': {'en': title},
        'contents': {'en': message},
    }
    if data:
        payload['data'] = data
    return _post(payload)


def notify_complaint_status_changed(complaint) -> None:
    """Notify the user that their complaint status has been updated."""
    player_id = complaint.user.onesignal_player_id
    if not player_id:
        return
    send_to_user(
        player_id=player_id,
        title='Complaint Update',
        message=f'Your complaint "{complaint.title}" status changed to: {complaint.get_status_display()}.',
        data={'complaint_id': complaint.id, 'status': complaint.status},
    )


def notify_news_published(title: str, body: str) -> None:
    """Notify all users of a new news article."""
    send_to_all(
        title='New Announcement',
        message=title,
        data={'type': 'news'},
    )


def _post(payload: dict) -> dict:
    try:
        response = requests.post(ONESIGNAL_API_URL, json=payload, headers=_build_headers(), timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return {}
