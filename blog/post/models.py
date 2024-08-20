from django.db import models
from user.models import User


# Create your models here.
class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50, null=False, blank=False)
    content = models.CharField(max_length=500, null=False)
    author = models.ForeignKey(User, related_name="post", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"author: {self.author} title: {self.title} is created"
