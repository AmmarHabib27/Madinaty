from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from base.serializers.client import CategorySerializer
from base.services.admin import categoryService
from base.pagination import StandardPagination


class CategoryListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categories = categoryService.list_categories().filter(is_active=True)
        paginator = StandardPagination()
        page = paginator.paginate_queryset(categories, request)
        serializer = CategorySerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
