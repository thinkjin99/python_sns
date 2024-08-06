import json
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.views import View
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect

from response.exceptions import UnAuthorizedException, UnProcessableException
from response.validator import ResponseValidator

from .auth.jwt_ import JWT
from .forms import LoginForm, RegisterForm
from .models import User, RefreshToken
from response.validator import ResponseValidator


class RegisterView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = RegisterForm()
        return render(request, "register.html", {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse | HttpResponse:
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            User.objects.create_user(**data)  # type: ignore
            return redirect("/user/login")
        else:
            return render(
                request, "register.html", {"form": form}, status=201
            )  # 에러를 포함해 재 렌더링


class RefreshView(View):
    def post(self, request: HttpRequest) -> ResponseValidator:
        body = json.loads(request.body)
        access_token = body["access_token"]
        response = ResponseValidator(message="Success", status=201)

        if not access_token:
            raise UnProcessableException

        jwt = JWT()
        if payload := jwt.decode(access_token, verify_exp=False):
            new_token = jwt.encode({"id": payload.id, "is_refresh": False})
            response.data = {"access_token": new_token}
            return response
        else:
            raise UnAuthorizedException


class LoginView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, reqeust: HttpRequest) -> ResponseValidator:
        """
        포스트 API로 리퀘스트에서 인증 정보를 추출해 확인하고 이를 토대로 jwt 토큰을 발급합니다.

        Args:
            reqeust (HttpRequest): 로그인 인증 정보

        Returns:
            JsonResponse: jwt 토큰
        """
        form = LoginForm(reqeust.POST)
        response = ResponseValidator(message="Success", status=201)

        if not form.is_valid():
            raise UnProcessableException  # form을 또 사용할지 모르겠음

        data = form.cleaned_data
        email, password = (
            data["email"],
            data["password"],
        )  # 딕셔너리를 통해서 접근하는거 강인한 DTO가 아님.

        if not (user := authenticate(username=email, password=password)):
            raise UnAuthorizedException

        access_token = JWT().encode(payload={"id": user.pk, "is_refresh": False})
        refresh_token = JWT().encode(payload={"id": user.pk, "is_refresh": True})

        RefreshToken.objects.filter(user=user).update_or_create(
            user=user, token=refresh_token
        )  # upsert refresh token

        data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
        response.data = data
        return response
