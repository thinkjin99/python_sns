from django.db import models
from user.models import User
from post.models import Post

# Create your models here.


class Comment(models.Model):
    author = models.ForeignKey(
        User, related_name="user_comment", on_delete=models.SET_NULL, null=True
    )
    post = models.ForeignKey(
        Post, related_name="post_comment", on_delete=models.CASCADE
    )
    content = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
