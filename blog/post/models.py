from django.db import models
from user.models import User


# Create your models here.
class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50, null=False, blank=False)
    content = models.CharField(max_length=500, null=False)
    # gaechu = models.DecimalField(max_digits=100000000) image를 추가해보는 건..?
    author = models.ForeignKey(User, related_name="post", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"author: {self.author} title: {self.title} is created"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author": self.author_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class Comment(models.Model):
    author = models.ForeignKey(
        User, related_name="user_comment", on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post, related_name="post_comment", on_delete=models.CASCADE
    )
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
