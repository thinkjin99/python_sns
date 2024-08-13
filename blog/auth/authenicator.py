from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from user.models import User
from .jwt_ import JWT, jwt


class JWTAuthenicator(BaseAuthentication):
    """
    JWT 인증을 진행하는 커스텀 인증기 입니다.

    Args:
        BaseAuthentication (_type_): _description_
    """

    def get_user(self, user_id: int) -> User:
        user = User.objects.get(id=user_id)
        return user

    def authenticate(self, request):
        auth_header: str = request.headers["Authorization"]
        protocol, _, token = auth_header.partition(" ")
        if protocol.lower() != "bearer":
            raise AuthenticationFailed
        try:
            payload = JWT.decode(token)
            request.payload = payload
            user = self.get_user(user_id=payload.id)
            return (user, None)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token")

        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

    # def authenticate_header(self, request):
    # return "Bearer"
