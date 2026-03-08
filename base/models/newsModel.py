from django.db import models
from django.utils import timezone


class News(models.Model):
    created_by = models.ForeignKey(
        'base.Admin',
        on_delete=models.SET_NULL,
        null=True,
        related_name='news_posts'
    )
    title = models.CharField(max_length=255)
    body = models.TextField()
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)
    start_date = models.DateTimeField()
    expiry_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'news'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.expiry_date
