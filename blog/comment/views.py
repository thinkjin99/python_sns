from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


from .models import Comment
from .serializers import CommentSerializer
from .filters import CommentFilter
from auth.authenicator import JWTAuthenicator
from permissions.author import IsAuthorOrReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    # 해당 뷰에서는 코멘트의 추가,수정,삭제,개별 조회만 가능해야 한다.
    authentication_classes = [JWTAuthenicator]
    permission_classes = [IsAuthorOrReadOnly]
    serializer_class = CommentSerializer
    # filterset_class = CommentFilter
    queryset = Comment.objects.all()

    @action(detail=True, methods=["GET"])
    def post_list(self, *args, **kwargs):
        self.lookup_field = "post_id"
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(
            queryset, many=True
        )  # 쿼리셋을 집어넣었는데 유효성 검사를 할 필요는 없다, 쿼리셋의 직렬화를 위해서만 사용
        return Response(serializer.data)
