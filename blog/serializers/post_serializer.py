from rest_framework import serializers
from post.models import Post
from user.models import User


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "content", "author"]

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=50, required=True)
    content = serializers.CharField(max_length=500, required=True)
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True
    )

    # def validate_author(self, value):
    #     try:
    #         user = User.objects.get(id=value)
    #         return value

    #     except User.DoesNotExist as e:
    #         raise serializers.ValidationError("User is not exists")
