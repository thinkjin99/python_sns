import logging
import pytest

from django.test import Client
from django.urls import reverse

from .fixtures import user
from user.models import User

logger = logging.getLogger("test")


@pytest.mark.django_db
class TestUser:
    def test_crate_user(self):
        data = {"email": "abc@naver.com", "password": "a123", "profile_id": "a123"}
        user = User.objects.create_user(**data)
        user.follows.add(user)

    def test_login(self, user):
        url = reverse("user:login")
        data = {"email": user.get("email"), "password": user.get("password")}
        client = Client()
        response = client.post(
            path=url,
            data=data,
        )
        logging.info(f"header: {response.headers} data: {response.json()}")
        assert response.status_code == 201
