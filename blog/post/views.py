import json

from django.http import HttpRequest

from user.auth.auth_mixin import JWTRequiredView
from response.validator import ResponseValidator
from response.exceptions import (
    UnProcessableException,
    NotFoundException,
    UnAuthorizedException,
)

from .models import Post
from .validator import PostValidator
from .selectors.post_selector import get_following_post_by_page


def json_api(func):
    def wraaper(*args, **kwargs):
        response = ResponseValidator(message="success", status=200)
        status, data = func(*args, **kwargs)
        response.status = status
        response.data = data
        return response

    return wraaper


class PostView(JWTRequiredView):
    @json_api
    def get(self, request: HttpRequest, post_id: int) -> tuple[int, dict]:
        try:
            post = Post.objects.get(id=post_id)
            return 200, post.to_dict()

        except Post.DoesNotExist:
            raise NotFoundException

    @json_api
    def post(self, request: HttpRequest) -> tuple[int, dict]:
        try:
            body = json.loads(request.body)
            body.update({"author_id": self.payload.id})  # update user id

            post_data = PostValidator(**body)
            post = Post.objects.create(**post_data.model_dump())
            return 201, post.to_dict()

        except (json.JSONDecodeError, ValueError):
            raise UnProcessableException

    @json_api
    def put(self, request: HttpRequest, post_id: int) -> tuple[int, dict]:
        try:
            post = Post.objects.get(id=post_id)
            if self.payload.id != post.author_id:
                raise UnAuthorizedException

            body = json.loads(request.body)
            body.update({"author_id": self.payload.id})  # update user id

            post_data = PostValidator(**body)
            Post.objects.filter(id=post_id).update(**post_data.model_dump())
            return 200, post_data.model_dump()

        except Post.DoesNotExist:
            raise NotFoundException

    @json_api
    def delete(self, request: HttpRequest, post_id: int):
        try:
            post = Post.objects.get(id=post_id)
            if self.payload.id != post.author_id:
                raise UnAuthorizedException

            post = post.delete()
            return 200, post

        except Post.DoesNotExist:
            raise NotFoundException


class PostListView(JWTRequiredView):
    @json_api
    def get(self, request: HttpRequest) -> tuple[int, dict]:
        try:
            page_num = int(request.GET["page"])
            data = get_following_post_by_page(self.payload.id, page_num)
            return 200, data

        except ValueError:
            raise UnProcessableException
