from django.db import models


class Category(models.Model):
    created_by = models.ForeignKey(
        'base.Admin',
        on_delete=models.SET_NULL,
        null=True,
        related_name='categories'
    )
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
