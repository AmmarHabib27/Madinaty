from rest_framework.exceptions import NotFound
from base.models import News


def list_news():
    return News.objects.select_related('created_by').order_by('-created_at')


def get_news(news_id: int) -> News:
    try:
        return News.objects.select_related('created_by').get(id=news_id)
    except News.DoesNotExist:
        raise NotFound('News article not found.')


def create_news(admin_user, validated_data: dict) -> News:
    return News.objects.create(created_by=admin_user, **validated_data)


def update_news(news_id: int, validated_data: dict) -> News:
    news = get_news(news_id)
    for attr, value in validated_data.items():
        setattr(news, attr, value)
    news.save()
    return news


def delete_news(news_id: int) -> None:
    news = get_news(news_id)
    news.delete()
