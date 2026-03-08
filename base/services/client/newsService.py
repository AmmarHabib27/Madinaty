from django.utils import timezone
from base.models import News


def list_active_news():
    now = timezone.now()
    return News.objects.filter(start_date__lte=now, expiry_date__gte=now)


def get_news(news_id: int) -> News:
    from rest_framework.exceptions import NotFound
    now = timezone.now()
    try:
        return News.objects.get(id=news_id, start_date__lte=now, expiry_date__gte=now)
    except News.DoesNotExist:
        raise NotFound('News article not found or not yet active / has expired.')
