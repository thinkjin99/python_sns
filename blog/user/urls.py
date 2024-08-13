from django.urls import path
from user.views import LoginView, RegisterView, RefreshTokenView

app_name = "user"
urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("register", RegisterView.as_view(), name="register"),
    path("refresh", RefreshTokenView.as_view(), name="refresh"),
]
