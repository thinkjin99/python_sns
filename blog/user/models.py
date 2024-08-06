from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class UserManager(BaseUserManager):
    def create_user(self, email: str, profile_id: str, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, profile_id=profile_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email: str, profile_id: str, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        self.create_user(email, profile_id, password, **extra_fields)


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    profile_id = models.CharField(max_length=30, null=False, blank=False, unique=True)
    email = models.EmailField(max_length=40, null=False, blank=False, unique=True)
    password = models.CharField(max_length=200, null=False)
    is_staff = models.BooleanField(("staff status"), default=False)
    is_active = models.BooleanField(("active"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    follows = models.ManyToManyField(
        "self", related_name="followd_by", symmetrical=False
    )  # django의 m-m은 자동으로 cascade 삭제

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["profile_id"]

    def __str__(self):
        return f"{self.profile_id} {self.created_at}"


class RefreshToken(models.Model):
    user = models.ForeignKey(User, related_name="token", on_delete=models.CASCADE)
    token = models.CharField(max_length=300, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
