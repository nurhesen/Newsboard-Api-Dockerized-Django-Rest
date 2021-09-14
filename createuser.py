from django.contrib.auth.models import User
from api.models import Author
from api.models import NewsModel
try:
    usr=User.objects.create_superuser('test', 'test@example.com', 'test')
    authr=Author.objects.create(name="Authorname", last_name="Authorlastname", user=usr)
    news=NewsModel.objects.create(news_title="Title of new news", news_content="Content of news. It can be as long as you want", news_author=authr)

except:
    pass