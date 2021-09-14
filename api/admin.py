from django.contrib import admin
from .models import Author, NewsModel, Upvote, Comment

# Register your models here.

admin.site.register(Author)
admin.site.register(NewsModel)
admin.site.register(Upvote)
admin.site.register(Comment)
