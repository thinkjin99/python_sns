import json
import logging
import pytest

from django.test import Client
from django.urls import reverse

from .fixtures import login_token, post, posts
from user.models import User

logger = logging.getLogger("test")

TEST_USER_ID = "abc@naver.com"
TEST_USER_PASSWORD = "a123"
TEST_PROFILE_ID = "Test"


def create_user(user_id: str, password: str, profile_id: str) -> dict:
    data = {"email": user_id, "password": password, "profile_id": profile_id}
    user = User.objects.create_user(**data)
    user.follows.add(user)
    return data


def login(username, password) -> dict:
    url = reverse("user:login")
    data = {"email": username, "password": password}
    client = Client()
    response = client.post(
        path=url,
        data=data,
    )
    # logging.info(f"header: {response.headers} data: {response.json()}")
    assert response.status_code == 200

    data = response.json()
    return data


@pytest.mark.django_db
class TestPost:
    def test_post_post(self, login_token):
        access_token = login_token["access_token"]
        auth_header = {"Authorization": "Bearer " + access_token}
        post_data = {"title": "안녕하세요", "content": "나는 손범수"}
        url = reverse("post-list")
        client = Client()

        for _ in range(5):
            resp = client.post(
                path=url,
                data=post_data,
                content_type="application/json",
                headers=auth_header,
            )

            logging.info(f"Message: {json.loads(resp.content)}")
            assert resp.status_code == 201

    def test_get_post(self, login_token: dict, post: dict):
        access_token = login_token["access_token"]
        auth_header = {"Authorization": "Bearer " + access_token}
        url = reverse("post-detail", kwargs={"pk": 1})
        client = Client()
        resp = client.get(
            path=url,
            headers=auth_header,
        )
        assert resp.status_code == 200
        logging.info(f"Message: {json.loads(resp.content)}")

    def test_view_post_list(self, login_token, posts: list):
        access_token = login_token["access_token"]
        auth_header = {"Authorization": "Bearer " + access_token}
        url = reverse("post-list")
        client = Client()
        for i in range(1, 3):
            resp = client.get(path=url, headers=auth_header, QUERY_STRING=f"page={i}")
            assert resp.status_code == 200
            logging.info(f"Message: {json.loads(resp.content)}")

    def test_put_post(self, login_token: dict, post: dict):
        access_token = login_token["access_token"]
        auth_header = {"Authorization": "Bearer " + access_token}
        url = reverse("post-detail", kwargs={"pk": 1})
        client = Client()
        post_data = {
            "title": "안녕하세요",
            "content": "나는 손범수22",
        }
        resp = client.put(
            path=url,
            headers=auth_header,
            data=post_data,
            content_type="application/json",
        )
        assert resp.status_code == 201
        logging.info(f"Message: {json.loads(resp.content)}")

    def test_delete_post(self, login_token: dict, post: dict):
        access_token = login_token["access_token"]
        auth_header = {"Authorization": "Bearer " + access_token}
        url = reverse("post-detail", kwargs={"pk": 1})
        client = Client()
        resp = client.delete(
            path=url,
            headers=auth_header,
            content_type="application/json",
        )
        assert resp.status_code == 204
        logging.info(f"Message: Post successfully deleted")

    def test_non_author_delete(self, login_token, post):
        username = "test123@gmail.com"
        password = "abc1234"
        profile_id = "test1"
        user = create_user(username, password, profile_id)
        login_token = login(username, password)
        access_token = login_token["access_token"]
        auth_header = {"Authorization": "Bearer " + access_token}
        url = reverse("post-detail", kwargs={"pk": 1})
        client = Client()
        resp = client.delete(
            path=url,
            headers=auth_header,
            content_type="application/json",
        )
        assert resp.status_code == 403
        logging.info(f"Message: Correctly denied")

    def test_non_author_put(self, login_token, post):
        username = "test123@gmail.com"
        password = "abc1234"
        profile_id = "test1"
        user = create_user(username, password, profile_id)
        login_token = login(username, password)
        access_token = login_token["access_token"]
        auth_header = {"Authorization": "Bearer " + access_token}
        url = reverse("post-detail", kwargs={"pk": 1})
        client = Client()
        post_data = {
            "title": "안녕하세요",
            "content": "나는 손범수22",
        }
        resp = client.put(
            path=url,
            data=post_data,
            headers=auth_header,
            content_type="application/json",
        )
        assert resp.status_code == 403
        logging.info(f"Message: Correctly denied")
