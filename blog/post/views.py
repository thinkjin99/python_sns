from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


from .models import Post
from .serializers import PostSerializer
from auth.authenicator import JWTAuthenicator
from permissions.author import IsAuthorOrReadOnly


class PostPagination(PageNumberPagination):
    page_size = 5
    # page_query_param = "page_num"


class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthenicator]
    permission_classes = [IsAuthorOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    pagination_class = PostPagination

    # def create(self, request, *args, **kwargs):
    #     # request.data["author"] = request.user.id  # 인증 유저 아이디 추가
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     return Response(serializer.data, status=201)

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     request.data["author"] = request.user.id  # 인증 유저 아이디 추가
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data, status=200)
