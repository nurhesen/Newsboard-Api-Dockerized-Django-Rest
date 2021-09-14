from django.db import models
from django.contrib.auth.models import User

# from django.urls import reverse
from django.utils import timezone


class Author(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="author",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class NewsModel(models.Model):
    news_title = models.CharField(max_length=300)
    news_content = models.TextField()
    news_creation_date = models.DateTimeField(default=timezone.now)
    news_author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = [
            "news_creation_date",
        ]

    def __str__(self):
        return self.news_title


#    def get_url(self):
#      return reverse('news-detail', args=(self.pk,))


class Upvote(models.Model):
    upvoter = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="upvoted_news"
    )
    upvoted_news = models.ForeignKey(
        NewsModel, on_delete=models.CASCADE, related_name="upvoter"
    )

    class Meta:
        unique_together = (
            "upvoter",
            "upvoted_news",
        )


class Comment(models.Model):
    comment_author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="comments"
    )
    commented_news = models.ForeignKey(
        NewsModel,
        on_delete=models.CASCADE,
        related_name="comments",
        null=True,
        blank=True,
    )

    comment_content = models.TextField()
    comment_creation_date = models.DateTimeField(default=timezone.now)
