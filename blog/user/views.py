from rest_framework.views import APIView
from rest_framework import generics

from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.request import Request


# from response.exceptions import UnAuthorizedException, UnProcessableException
from serializers.user_serializer import LoginSerializer, RegisterSerializer


from auth.jwt_ import JWT
from .models import RefreshToken


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(status=201, data=serializer.data)


# class RefreshView(View):
#     def post(self, request: HttpRequest) -> ResponseValidator:
#         body = json.loads(request.body)
#         access_token = body["access_token"]
#         response = ResponseValidator(message="Success", status=201)

#         if not access_token:
#             raise UnProcessableException

#         jwt = JWT()
#         if payload := jwt.decode(access_token, verify_exp=False):
#             new_token = jwt.encode({"id": payload.id, "is_refresh": False})
#             response.data = {"access_token": new_token}
#             return response
#         else:
#             raise UnAuthorizedException


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request: Request) -> Response:
        """
        포스트 API로 리퀘스트에서 인증 정보를 추출해 확인하고 이를 토대로 jwt 토큰을 발급합니다.

        Args:
            reqeust (HttpRequest): 로그인 인증 정보

        Returns:
            JsonResponse: jwt 토큰
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 유효성 검사

        data = serializer.data
        email, password = (
            data.get("email"),
            data.get("password"),
        )

        if not (user := authenticate(username=email, password=password)):
            raise AuthenticationFailed

        access_token = JWT().encode(payload={"id": user.pk, "is_refresh": False})
        refresh_token = JWT().encode(payload={"id": user.pk, "is_refresh": True})

        RefreshToken.objects.filter(user=user).update_or_create(
            user=user, token=refresh_token
        )  # upsert refresh token

        data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
        response = Response(status=200, data=data)
        return response
