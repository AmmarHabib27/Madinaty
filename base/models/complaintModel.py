from django.db import models
from django.conf import settings


class ComplaintStatus(models.TextChoices):
    PLACED = 'placed', 'Placed'
    VALID = 'valid', 'Valid'
    ON_HOLD = 'on_hold', 'On Hold'
    REJECTED = 'rejected', 'Rejected'
    RESOLVED = 'resolved', 'Resolved'


class ComplaintPriority(models.TextChoices):
    LOW = 'low', 'Low'
    INTERMEDIATE = 'intermediate', 'Intermediate'
    HIGH = 'high', 'High'


class Complaint(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='complaints'
    )
    category = models.ForeignKey(
        'base.Category',
        on_delete=models.SET_NULL,
        null=True,
        related_name='complaints'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=ComplaintStatus.choices,
        default=ComplaintStatus.PLACED
    )
    priority = models.CharField(
        max_length=20,
        choices=ComplaintPriority.choices,
        default=ComplaintPriority.LOW
    )
    admin_comment = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_address = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'complaints'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} - {self.status}'


class ComplaintMedia(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = 'image', 'Image'
        VIDEO = 'video', 'Video'

    complaint = models.ForeignKey(
        Complaint,
        on_delete=models.CASCADE,
        related_name='media'
    )
    file = models.FileField(upload_to='complaint_media/')
    media_type = models.CharField(max_length=10, choices=MediaType.choices, default=MediaType.IMAGE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'complaint_media'

    def __str__(self):
        return f'{self.media_type} for complaint #{self.complaint.id}'
