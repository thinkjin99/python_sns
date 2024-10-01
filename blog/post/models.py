import datetime
from django.db import models

from user.models import User


def get_one_hour_from_now():
    return datetime.datetime.now() + datetime.timedelta(hours=1)


# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=50)


class Post(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    content = models.CharField(max_length=500, null=False)
    author = models.ForeignKey(User, related_name="post", on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING, blank=False, null=False)
    valid_time = models.DateTimeField(default=get_one_hour_from_now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"author: {self.author} title: {self.title} is created"
