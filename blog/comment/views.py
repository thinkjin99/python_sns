from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ParseError


from .models import Comment
from .serializers import (
    CommentGetSerializer,
    CommentCreateSerializer,
    CommentUpdateSerializer,
)
from auth.authenicator import JWTAuthenicator
from permissions.author import IsAuthorOrReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    # 해당 뷰에서는 코멘트의 추가,수정,삭제,개별 조회만 가능해야 한다.
    authentication_classes = [JWTAuthenicator]
    permission_classes = [IsAuthorOrReadOnly]
    serializer_class = CommentGetSerializer
    queryset = Comment.objects.all()

    # def get_serializer_class(self):
    #     if self.action == "create":
    #         return CommentCreateSerializer
    #     elif self.action == "update":
    #         return CommentUpdateSerializer
    #     return self.serializer_class

    @action(
        detail=True,
        methods=["GET"],
        url_path="posts/comments",
        serializer_class=CommentGetSerializer,
    )
    def list_post_comments(self, *args, **kwargs):
        self.lookup_field = "post_id"
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(
            queryset, many=True
        )  # 쿼리셋을 집어넣었는데 유효성 검사를 할 필요는 없다, 쿼리셋의 직렬화를 위해서만 사용
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        kwargs.setdefault("context", self.get_serializer_context())
        serializer = CommentCreateSerializer(data=request.data, **kwargs)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        return Response(data=serializer.data, status=201)

    # def list(self, request, *args, **kwargs):
    #     """
    #     기본 `list` 액션을 오버라이드하여 모든 `GET` 요청을 거부할 수 있습니다.
    #     """
    #     raise ParseError(detail="Missing Prameter comment_id")
