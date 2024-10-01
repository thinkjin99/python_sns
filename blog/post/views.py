from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import GenericAPIView, ListAPIView


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

