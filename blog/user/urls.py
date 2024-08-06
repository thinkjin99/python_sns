from django.urls import path
from user.views import LoginView, RegisterView

app_name = "user"
urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("register", RegisterView.as_view(), name="register"),
]
