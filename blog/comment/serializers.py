from rest_framework import serializers
from .models import Comment
from user.models import User


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "author", "post", "content", "created_at"]

    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True
    )
    cotent = serializers.CharField(max_length=100, required=True)
