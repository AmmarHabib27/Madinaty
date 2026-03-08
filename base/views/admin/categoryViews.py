from rest_framework.views import APIView
from base.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from base.serializers.admin import CategorySerializer, CategoryCreateSerializer
from base.services.admin import categoryService
from base.pagination import StandardPagination


class CategoryListCreateView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        categories = categoryService.list_categories()
        paginator = StandardPagination()
        page = paginator.paginate_queryset(categories, request)
        serializer = CategorySerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = CategoryCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = categoryService.create_category(request.user, serializer.validated_data)
        return Response(CategorySerializer(category).data, status=status.HTTP_201_CREATED)


class CategoryDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        category = categoryService.get_category(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def patch(self, request, pk):
        category = categoryService.get_category(pk)
        serializer = CategoryCreateSerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated = categoryService.update_category(pk, serializer.validated_data)
        return Response(CategorySerializer(updated).data)

    def delete(self, request, pk):
        categoryService.delete_category(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
