from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import Comment
from user.models import User


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "author", "post", "content", "created_at"]
        read_only_fields = ["author", "post", "created_at"]

    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), default=CurrentUserDefault()
    )
    cotent = serializers.CharField(max_length=100, required=True)
