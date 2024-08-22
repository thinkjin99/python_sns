from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import Comment
from user.models import User
from post.models import Post


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "author", "post", "content", "created_at"]
        read_only_fields = ["author", "post", "created_at"]

    post = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(), required=True
    )
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), default=CurrentUserDefault()
    )
    content = serializers.CharField(max_length=100, required=True)
