from rest_framework.exceptions import NotFound
from base.models import Complaint, ComplaintStatus, ComplaintPriority


def list_complaints(filters: dict = None):
    qs = Complaint.objects.select_related('user', 'category').prefetch_related('media').order_by('-created_at')
    if filters:
        if filters.get('status'):
            qs = qs.filter(status=filters['status'])
        if filters.get('priority'):
            qs = qs.filter(priority=filters['priority'])
        if filters.get('category_id'):
            qs = qs.filter(category_id=filters['category_id'])
    return qs


def list_all_complaints(filters: dict = None):
    qs = Complaint.objects.all().order_by('-created_at')
    if filters:
        if filters.get('status'):
            qs = qs.filter(status=filters['status'])
        if filters.get('priority'):
            qs = qs.filter(priority=filters['priority'])
        if filters.get('category_id'):
            qs = qs.filter(category_id=filters['category_id'])
    return qs


def get_complaint(complaint_id: int) -> Complaint:
    try:
        return Complaint.objects.select_related('user', 'category').prefetch_related('media').get(id=complaint_id)
    except Complaint.DoesNotExist:
        raise NotFound('Complaint not found.')


def update_complaint_status(complaint_id: int, validated_data: dict) -> Complaint:
    complaint = get_complaint(complaint_id)
    for attr, value in validated_data.items():
        setattr(complaint, attr, value)
    complaint.save()
    return complaint
