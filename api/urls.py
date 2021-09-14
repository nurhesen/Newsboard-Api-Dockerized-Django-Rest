from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CreateNewsView,
    ReadNewsView,
    NewsDetail,
    UpvoteView,
    CommentView,
    GetCommentsView,
    NewsPutDetail,
)


router = DefaultRouter()
router.register(r"create", CreateNewsView, basename="create-news")

urlpatterns = [
    path("read-list", ReadNewsView.as_view(), name="read-news-list"),
    path("detail-news/<int:pk>", NewsDetail.as_view()),
    path("detail-news-put/<int:pk>", NewsPutDetail.as_view()),
    path("upvote", UpvoteView.as_view()),
    path("comment", CommentView.as_view()),
    path("get-comment/<int:pk>", GetCommentsView.as_view()),
]


urlpatterns += router.urls
