import json
import base64

import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings
from django.db.models import Q


def _get_app():
    if not firebase_admin._apps:
        raw = settings.FCM_SERVICE_ACCOUNT_JSON
        if raw:
            decoded = base64.b64decode(raw).decode('utf-8')
            cred = credentials.Certificate(json.loads(decoded))
            firebase_admin.initialize_app(cred)
    return firebase_admin.get_app()


def send_to_all(title: str, message: str, data: dict = None) -> None:
    from base.models import User
    tokens = User.objects.exclude(Q(fcm_token='') | Q(fcm_token__isnull=True)).values_list('fcm_token', flat=True)
    for token in tokens:
        send_to_user(fcm_token=token, title=title, message=message, data=data)


def send_to_user(fcm_token: str, title: str, message: str, data: dict = None) -> None:
    if not fcm_token:
        return
    msg = messaging.Message(
        token=fcm_token,
        notification=messaging.Notification(title=title, body=message),
        data={k: str(v) for k, v in (data or {}).items()},
    )
    try:
        messaging.send(msg, app=_get_app())
    except Exception:
        pass


def notify_news_published(title: str, body: str) -> None:
    send_to_all(
        title='New Announcement',
        message=title,
        data={'type': 'news'},
    )


def notify_complaint_status_changed(complaint) -> None:
    fcm_token = complaint.user.fcm_token
    if not fcm_token:
        return
    send_to_user(
        fcm_token=fcm_token,
        title='Complaint Update',
        message=f'Your complaint "{complaint.title}" status changed to: {complaint.get_status_display()}.',
        data={'complaint_id': complaint.id, 'status': complaint.status},
    )
