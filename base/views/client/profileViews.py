from rest_framework.views import APIView
from base.permissions import IsRegularUser
from rest_framework.response import Response
from rest_framework import status

from base.serializers.client import ProfileSerializer, UpdateProfileSerializer
from base.services.client import profileService


class ProfileView(APIView):
    permission_classes = [IsRegularUser]

    def get(self, request):
        user = profileService.get_profile(request.user)
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UpdateProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = profileService.update_profile(request.user, serializer.validated_data)
        return Response(ProfileSerializer(user).data)


class DeleteProfilePictureView(APIView):
    permission_classes = [IsRegularUser]

    def delete(self, request):
        profileService.delete_profile_picture(request.user)
        return Response({'detail': 'Profile picture removed.'})
