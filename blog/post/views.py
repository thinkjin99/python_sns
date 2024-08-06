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


class PostView(JWTRequiredView):
    def get(self, request: HttpRequest, post_id: int) -> ResponseValidator:
        try:
            post = Post.objects.get(id=post_id)
            response = ResponseValidator.success(data=post.to_dict())
            return response

        except Post.DoesNotExist:
            raise NotFoundException

    def post(self, request: HttpRequest) -> ResponseValidator:
        try:
            body = json.loads(request.body)
            body.update({"author_id": self.payload.id})  # update user id

            post_data = PostValidator(**body).model_dump()
            post = Post.objects.create(**post_data)
            response = ResponseValidator.created(data=post.to_dict())
            return response

        except (json.JSONDecodeError, ValueError):
            raise UnProcessableException

    def put(self, request: HttpRequest, post_id: int) -> ResponseValidator:
        try:
            post = Post.objects.get(id=post_id)
            if self.payload.id != post.author_id:
                raise UnAuthorizedException

            body = json.loads(request.body)
            body.update({"author_id": self.payload.id})  # update user id

            post_data = PostValidator(**body).model_dump()
            Post.objects.filter(id=post_id).update(**post_data)
            response = ResponseValidator.created(data=post_data)
            return response

        except Post.DoesNotExist:
            raise NotFoundException

    def delete(self, request: HttpRequest, post_id: int) -> ResponseValidator:
        try:
            post = Post.objects.get(id=post_id)
            if self.payload.id != post.author_id:
                raise UnAuthorizedException

            post = post.delete()
            response = ResponseValidator.success(message="deleted", data=None)
            return response

        except Post.DoesNotExist:
            raise NotFoundException


class PostListView(JWTRequiredView):
    def get(self, request: HttpRequest) -> ResponseValidator:
        try:
            page_num = int(request.GET["page"])
            data = get_following_post_by_page(self.payload.id, page_num)
            response = ResponseValidator.success(data=data)
            return response

        except ValueError:
            raise UnProcessableException
