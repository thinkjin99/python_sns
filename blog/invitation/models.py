from django.db import models
from post.models import Post
from post.models import User

"""
특정 게시글에 대한 참여요청을 저장한다.
각 게시글 별로 해당 게시글에 참여 요청을 보낸 유저가 기록된다.
게시글에 유효 시간이 존재하기 때문에 해당 테이블에는 굳이 유효시간이 필요하지 않다.
"""


# Create your models here.
class InvitationRequest(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    requester = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    status = models.CharField(
        max_length=10, default="ISSUED"
    )  # ISSUE, PENDING, ACCEPT, REJECT
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
