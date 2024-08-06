from django.urls import path
from .views import PostView, PostListView

app_name = "post"
urlpatterns = [
    path("<int:post_id>", PostView.as_view(), name="view"),
    path("", PostView.as_view(), name="create"),
    path("list", PostListView.as_view(), name="list"),
]
