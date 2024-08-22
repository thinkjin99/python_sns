from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet
from comment.views import CommentViewSet

router = DefaultRouter()
router.register(r"", PostViewSet, basename="post")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "comments/<int:post_id>",
        CommentViewSet.as_view({"get": "post_list"}),
        name="post-comment",
    ),
]
