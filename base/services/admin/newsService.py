from datetime import timedelta
from django.utils import timezone
from rest_framework.exceptions import NotFound
from base.models import News


def list_news():
    return News.objects.select_related('admin').order_by('-created_at')


def get_news(news_id: int) -> News:
    try:
        return News.objects.select_related('admin').get(id=news_id)
    except News.DoesNotExist:
        raise NotFound('News article not found.')


def create_news(admin_user, validated_data: dict) -> News:
    duration_hours = validated_data['duration_hours']
    validated_data['expiry_at'] = timezone.now() + timedelta(hours=duration_hours)
    return News.objects.create(admin=admin_user, **validated_data)


def update_news(news_id: int, validated_data: dict) -> News:
    news = get_news(news_id)
    if 'duration_hours' in validated_data:
        validated_data['expiry_at'] = timezone.now() + timedelta(hours=validated_data['duration_hours'])
    for attr, value in validated_data.items():
        setattr(news, attr, value)
    news.save()
    return news


def delete_news(news_id: int) -> None:
    news = get_news(news_id)
    news.delete()
