from django.urls import path, include

from rest_framework_nested import routers

from .views import PostViewSet
from comment.views import CommentViewSet


router = routers.SimpleRouter()
router.register(r"", PostViewSet)

comment_router = routers.NestedSimpleRouter(router, r"", lookup="post")
comment_router.register(r"comments", CommentViewSet, basename="post-comment")

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(comment_router.urls)),
]
