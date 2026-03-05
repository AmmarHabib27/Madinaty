from django.db import models
from django.conf import settings
from django.utils import timezone


class News(models.Model):
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='news_posts'
    )
    title = models.CharField(max_length=255)
    body = models.TextField()
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    duration_hours = models.PositiveIntegerField()
    expiry_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'news'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def is_expired(self):
        return timezone.now() > self.expiry_at
