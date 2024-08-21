import logging
import pytest

from django.test import Client
from django.urls import reverse

from .fixtures import login_token, TEST_PROFILE_ID, TEST_USER_ID, TEST_USER_PASSWORD
from user.models import User

logger = logging.getLogger("test")


@pytest.mark.django_db
class TestUser:

    def test_register(self):
        url = reverse("user:register")
        data = {
            "email": TEST_USER_ID,
            "password": TEST_USER_PASSWORD,
            "profile_id": TEST_PROFILE_ID,
        }
        client = Client()
        response = client.post(path=url, data=data)
        # user.follows.add(user)
        logging.info(f"header: {response.headers} data: {response.json()}")
        assert response.status_code == 201

    def test_login(self):
        url = reverse("user:login")
        data = {"email": TEST_USER_ID, "password": TEST_USER_PASSWORD}
        client = Client()
        response = client.post(
            path=url,
            data=data,
        )
        logging.info(f"header: {response.headers} data: {response.json()}")
        assert response.status_code == 200

    def test_refresh(self, login_token):
        url = reverse("user:refresh")
        refresh_token = login_token["refresh_token"]
        data = {"token": refresh_token}
        client = Client()

        response = client.post(path=url, data=data)
        logging.info(f"header: {response.headers} data: {response.json()}")
        assert response.status_code == 201
