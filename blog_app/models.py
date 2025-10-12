from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)


# for items in response:
# ...     BlogPost(title=items["title"], subtitle=items["subtitle"], content=items["content"], author=db[1]).save()