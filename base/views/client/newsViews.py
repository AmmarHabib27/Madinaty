from rest_framework.views import APIView
from base.permissions import IsRegularUser
from rest_framework.response import Response

from base.serializers.client import NewsListSerializer, NewsDetailSerializer
from base.services.client import newsService
from base.pagination import StandardPagination


class NewsListView(APIView):
    permission_classes = [IsRegularUser]

    def get(self, request):
        news = newsService.list_active_news()
        paginator = StandardPagination()
        page = paginator.paginate_queryset(news, request)
        serializer = NewsListSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


class NewsDetailView(APIView):
    permission_classes = [IsRegularUser]

    def get(self, request, pk):
        news = newsService.get_news(pk)
        serializer = NewsDetailSerializer(news, context={'request': request})
        return Response(serializer.data)
