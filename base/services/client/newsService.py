from django.utils import timezone
from base.models import News


def list_active_news():
    return News.objects.filter(is_active=True, expiry_at__gt=timezone.now())


def get_news(news_id: int) -> News:
    from rest_framework.exceptions import NotFound
    try:
        return News.objects.get(id=news_id, is_active=True, expiry_at__gt=timezone.now())
    except News.DoesNotExist:
        raise NotFound('News article not found or has expired.')
