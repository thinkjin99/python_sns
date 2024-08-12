from rest_framework import serializers
from post.models import Post
from user.models import User


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "content", "author"]

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=50)
    content = serializers.CharField(max_length=500)
    author = serializers.PrimaryKeyRelatedField(read_only=True, queryset=User)
