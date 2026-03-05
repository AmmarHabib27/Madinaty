from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from base.serializers.client import NewsListSerializer, NewsDetailSerializer
from base.services.client import newsService


class NewsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        news = newsService.list_active_news()
        serializer = NewsListSerializer(news, many=True, context={'request': request})
        return Response(serializer.data)


class NewsDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        news = newsService.get_news(pk)
        serializer = NewsDetailSerializer(news, context={'request': request})
        return Response(serializer.data)
