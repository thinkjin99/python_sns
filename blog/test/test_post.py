import json
import logging
import pytest

from django.test import Client
from django.urls import reverse

from .fixtures import jwt_token, user, post, posts

logger = logging.getLogger("test")


@pytest.mark.django_db
class TestPost:
    def test_post_post(self, jwt_token: str):
        auth_header = {"Authorization": "Bearer " + jwt_token}
        post_data = {
            "title": "안녕하세요",
            "content": "나는 손범수",
        }
        url = reverse("post:create")
        client = Client()

        for _ in range(10):
            resp = client.post(
                path=url,
                data=post_data,
                content_type="application/json",
                headers=auth_header,
            )
            logging.info(f"Message: {json.loads(resp.content)}")
            assert resp.status_code == 201

    def test_get_post(self, jwt_token: str, post: dict):
        auth_header = {"Authorization": "Bearer " + jwt_token}
        url = reverse("post:view", kwargs={"post_id": 1})
        client = Client()
        resp = client.get(
            path=url,
            headers=auth_header,
        )
        assert resp.status_code == 200
        logging.info(f"Message: {json.loads(resp.content)}")

    def test_view_post_list(self, jwt_token, posts: list):
        auth_header = {"Authorization": "Bearer " + jwt_token}
        url = reverse("post:list")
        client = Client()
        for i in range(1, 4):
            resp = client.get(path=url, headers=auth_header, QUERY_STRING=f"page={i}")
            assert resp.status_code == 200
            logging.info(f"Message: {json.loads(resp.content)}")

    def test_put_post(self, jwt_token: str, post: dict):
        auth_header = {"Authorization": "Bearer " + jwt_token}
        url = reverse("post:view", kwargs={"post_id": 1})
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
        assert resp.status_code == 200
        logging.info(f"Message: {json.loads(resp.content)}")

    def test_delete_post(self, jwt_token: str, post: dict):
        auth_header = {"Authorization": "Bearer " + jwt_token}
        url = reverse("post:view", kwargs={"post_id": 1})
        client = Client()
        resp = client.delete(
            path=url,
            headers=auth_header,
            content_type="application/json",
        )
        assert resp.status_code == 200
        logging.info(f"Message: {json.loads(resp.content)} deleted")
