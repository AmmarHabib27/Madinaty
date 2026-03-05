from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from base.serializers.admin import NewsSerializer, NewsCreateSerializer, NewsUpdateSerializer
from base.services.admin import newsService, notificationService


class AdminNewsListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        news_list = newsService.list_news()
        serializer = NewsSerializer(news_list, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = NewsCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        news = newsService.create_news(request.user, serializer.validated_data)
        notificationService.notify_news_published(news.title, news.body)
        return Response(NewsSerializer(news, context={'request': request}).data, status=status.HTTP_201_CREATED)


class AdminNewsDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        news = newsService.get_news(pk)
        serializer = NewsSerializer(news, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, pk):
        serializer = NewsUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        news = newsService.update_news(pk, serializer.validated_data)
        return Response(NewsSerializer(news, context={'request': request}).data)

    def delete(self, request, pk):
        newsService.delete_news(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
