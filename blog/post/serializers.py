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
        read_only=True
        # queryset=User.objects.all(), default=CurrentUserDefault()
    )

    def create(self, validated_data):
        validated_data["author"] = self.context[
            "request"
        ].user  # author값은 시스템에서 자동 초기화 해야한다. read_only는 save에 포함되지 않는다.
        return super().create(validated_data)
