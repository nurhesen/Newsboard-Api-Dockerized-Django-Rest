from rest_framework import serializers
from .models import NewsModel, Author, Upvote, Comment


class CreateNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsModel
        fields = (
            "news_title",
            "news_content",
        )

    def create(self, validated_data):
        author_news = Author.objects.get(user=self.context["request"].user.id)
        validated_data["news_author"] = author_news
        return super(CreateNewsSerializer, self).create(validated_data)


class NewsSerializer(serializers.ModelSerializer):
    upvote_count = serializers.SerializerMethodField("get_upvote_count")

    class Meta:
        model = NewsModel
        fields = (
            "news_title",
            "news_content",
            "news_author",
            "upvote_count",
            "id",
        )
        read_only_fields = [
            "upvote_count",
            "id",
        ]

    def get_upvote_count(self, value):
        return value.upvoter.count()


class NewsPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsModel
        fields = (
            "news_title",
            "news_content",
        )


class UpvoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upvote
        fields = ("upvoter", "upvoted_news")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("comment_author", "comment_content", "commented_news")
