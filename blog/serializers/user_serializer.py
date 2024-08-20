import re

from rest_framework import serializers
from user.models import User, RefreshToken
from auth.jwt_ import JWT


class RefreshTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefreshToken
        fields = ["user", "token"]

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )
    token = serializers.CharField(required=True)

    def validate_token(self, value):
        try:
            # 토큰 디코딩 및 payload에서 user_id 추출
            payload = JWT.decode(value, is_refresh=True)
            user_id = payload.id

            # user 필드를 설정하기 위해 user 객체를 가져옴
            user = User.objects.get(id=user_id)

            # user 필드를 수동으로 설정
            self.context["user"] = user
            return value

        except Exception as e:
            raise serializers.ValidationError(f"Invalid token: {str(e)}")

    def validate(self, attrs):
        # context에 저장한 user를 user 필드에 할당
        user = self.context.get("user")
        if user and User.objects.filter(id=user.id).exists():
            attrs["user"] = self.context["user"]  # 여기서 검증할 것 같음
            return attrs

        raise serializers.ValidationError("User does not exist")


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=40)
    password = serializers.CharField(required=True, max_length=20)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "profile_id", "email", "password"]

    profile_id = serializers.CharField(max_length=30)
    email = serializers.EmailField(required=True, max_length=40)
    password = serializers.CharField(required=True, write_only=True, max_length=20)

    def validate_profile_id(self, value):
        patt = r"[A-Za-z0-9_.]{3,30}"
        anti_patt = r"[^A-Za-z0-9_.]"
        if re.search(anti_patt, value):
            raise serializers.ValidationError("Only alphanumeric and -. is allowed")

        matched = re.match(patt, value)
        if not matched:
            raise serializers.ValidationError("profile_id is must between 3, 30")

        if User.objects.filter(profile_id=value).exists():
            raise serializers.ValidationError
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError
        return value
