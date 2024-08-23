from rest_framework import serializers

from .models import Comment
from post.models import Post


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ["id", "author", "post", "content", "created_at"]

    id = serializers.IntegerField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(), required=True
    )
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    content = serializers.CharField(max_length=100, required=True)

    def create(self, validated_data):
        validated_data["author"] = self.context[
            "request"
        ].user  # author값은 시스템에서 자동 초기화 해야한다. read_only는 save에 포함되지 않는다.
        return super().create(validated_data)


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "author", "post", "content", "created_at"]

    id = serializers.IntegerField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    content = serializers.CharField(max_length=100, required=True)


class CommentGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "author", "post", "content", "created_at"]
