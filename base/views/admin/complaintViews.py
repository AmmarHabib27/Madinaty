from rest_framework.views import APIView
from base.permissions import IsAdminUser
from rest_framework.response import Response

from base.serializers.admin import (
    AdminComplaintListSerializer,
    AdminComplaintDetailSerializer,
    UpdateComplaintStatusSerializer,
)
from base.services.admin import complaintService, notificationService
from base.pagination import StandardPagination


class AdminComplaintListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        filters = {
            'status': request.query_params.get('status'),
            'priority': request.query_params.get('priority'),
            'category_id': request.query_params.get('category_id'),
        }
        complaints = complaintService.list_complaints(filters)
        paginator = StandardPagination()
        page = paginator.paginate_queryset(complaints, request)
        serializer = AdminComplaintListSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


class AdminComplaintDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        complaint = complaintService.get_complaint(pk)
        serializer = AdminComplaintDetailSerializer(complaint, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, pk):
        serializer = UpdateComplaintStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        complaint = complaintService.update_complaint_status(pk, serializer.validated_data)
        notificationService.notify_complaint_status_changed(complaint)
        return Response(AdminComplaintDetailSerializer(complaint, context={'request': request}).data)
