from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from .serializers import (
    CreateNewsSerializer,
    NewsSerializer,
    UpvoteSerializer,
    CommentSerializer,
    NewsPutSerializer,
)
from .models import NewsModel
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status


class CreateNewsView(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = CreateNewsSerializer


class ReadNewsView(ListAPIView):
    serializer_class = NewsSerializer
    queryset = NewsModel.objects.all()


class NewsPutDetail(APIView):
    def get_object(self, pk):
        try:
            return NewsModel.objects.get(pk=pk)
        except NewsModel.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        if snippet.news_author.user.id != request.user.id:
            raise Http404
        serializer = NewsPutSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewsDetail(APIView):
    def get_object(self, pk):
        try:
            return NewsModel.objects.get(pk=pk)
        except NewsModel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = NewsSerializer(snippet)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        if snippet.news_author.user.id != request.user.id:
            raise Http404
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpvoteView(APIView):
    def post(self, request, format=None):
        request.data["upvoter"] = request.user.author.id
        serializer = UpvoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentView(APIView):
    def post(self, request, format=None):
        request.data["comment_author"] = request.user.author.id
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetCommentsView(APIView):
    def get_object(self, pk):
        try:
            return NewsModel.objects.get(pk=pk)
        except NewsModel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        print(dir(snippet.comments))
        print(snippet.comments.all())
        serializer = CommentSerializer(snippet.comments.all(), many=True)
        return Response(serializer.data)
