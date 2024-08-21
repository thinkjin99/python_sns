from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import Post
from user.models import User


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "content", "author", "created_at"]

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=50, required=True)
    content = serializers.CharField(max_length=500, required=True)
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), default=CurrentUserDefault()
    )
