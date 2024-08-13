import logging
import pytest

from django.test import Client
from django.urls import reverse

from .fixtures import user, jwt_token
from user.models import User

logger = logging.getLogger("test")


@pytest.mark.django_db
class TestUser:

    def test_register(self):
        url = reverse("user:register")
        data = {"email": "abc@naver.com", "password": "a123", "profile_id": "a123"}
        client = Client()
        response = client.post(path=url, data=data)
        # user.follows.add(user)
        logging.info(f"header: {response.headers} data: {response.json()}")
        assert response.status_code == 201

    def test_login(self, user):
        url = reverse("user:login")
        data = {"email": user.get("email"), "password": user.get("password")}
        client = Client()
        response = client.post(
            path=url,
            data=data,
        )
        logging.info(f"header: {response.headers} data: {response.json()}")
        assert response.status_code == 200

    def test_refresh(self, jwt_token):
        url = reverse("user:refresh")
        refresh_token = jwt_token["refresh_token"]
        data = {"token": refresh_token}
        client = Client()

        response = client.post(path=url, data=data)
        logging.info(f"header: {response.headers} data: {response.json()}")
        assert response.status_code == 201
