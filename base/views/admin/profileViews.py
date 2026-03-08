from rest_framework.views import APIView
from base.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from base.serializers.admin import (
    AdminProfileSerializer,
    AdminUpdateProfileSerializer,
    UserListSerializer,
)
from base.services.admin import profileService
from base.pagination import StandardPagination


class AdminProfileView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        serializer = AdminProfileSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = AdminUpdateProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = profileService.update_admin_profile(request.user, serializer.validated_data)
        return Response(AdminProfileSerializer(user).data)


class UserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = profileService.list_users()
        paginator = StandardPagination()
        page = paginator.paginate_queryset(users, request)
        serializer = UserListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class ToggleUserActiveView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        user = profileService.toggle_user_active(pk)
        return Response({
            'detail': f"User {'activated' if user.is_active else 'deactivated'} successfully.",
            'is_active': user.is_active,
        })
