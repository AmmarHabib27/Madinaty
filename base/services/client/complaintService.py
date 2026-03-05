from rest_framework.exceptions import NotFound, PermissionDenied
from base.models import Complaint, ComplaintMedia


def list_complaints(user):
    return Complaint.objects.filter(user=user).select_related('category')


def get_complaint(user, complaint_id: int) -> Complaint:
    try:
        return Complaint.objects.select_related('category').prefetch_related('media').get(
            id=complaint_id, user=user
        )
    except Complaint.DoesNotExist:
        raise NotFound('Complaint not found.')


def create_complaint(user, validated_data: dict) -> Complaint:
    media_files = validated_data.pop('media', [])
    complaint = Complaint.objects.create(user=user, **validated_data)
    _save_media(complaint, media_files)
    return complaint


def _save_media(complaint: Complaint, media_files: list) -> None:
    for file in media_files:
        content_type = getattr(file, 'content_type', '')
        if 'video' in content_type:
            media_type = ComplaintMedia.MediaType.VIDEO
        else:
            media_type = ComplaintMedia.MediaType.IMAGE
        ComplaintMedia.objects.create(complaint=complaint, file=file, media_type=media_type)


def delete_complaint(user, complaint_id: int) -> None:
    try:
        complaint = Complaint.objects.get(id=complaint_id, user=user)
    except Complaint.DoesNotExist:
        raise NotFound('Complaint not found.')
    complaint.delete()
