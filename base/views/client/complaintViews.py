from rest_framework.views import APIView
from base.permissions import IsRegularUser
from rest_framework.response import Response
from rest_framework import status

from base.serializers.client import (
    ComplaintListSerializer,
    ComplaintDetailSerializer,
    ComplaintCreateSerializer,
)
from base.services.client import complaintService
from base.pagination import StandardPagination


class ComplaintListCreateView(APIView):
    permission_classes = [IsRegularUser]

    def get(self, request):
        complaints = complaintService.list_complaints(request.user)
        paginator = StandardPagination()
        page = paginator.paginate_queryset(complaints, request)
        serializer = ComplaintListSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ComplaintCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        validated_data['media'] = request.FILES.getlist('media_files')
        complaint = complaintService.create_complaint(request.user, validated_data)
        return Response(
            ComplaintDetailSerializer(complaint, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )


class ComplaintDetailView(APIView):
    permission_classes = [IsRegularUser]

    def get(self, request, pk):
        complaint = complaintService.get_complaint(request.user, pk)
        serializer = ComplaintDetailSerializer(complaint, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, pk):
        complaintService.delete_complaint(request.user, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
