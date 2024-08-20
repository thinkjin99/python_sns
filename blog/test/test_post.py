import json
import logging
import pytest

from django.test import Client
from django.urls import reverse

from .fixtures import login_result, user, post, posts

logger = logging.getLogger("test")


@pytest.mark.django_db
class TestPost:
    def test_post_post(self, login_result: dict):
        access_token = login_result["access_token"]
        auth_header = {"Authorization": "Bearer " + access_token}
        post_data = {"title": "안녕하세요", "content": "나는 손범수"}
        url = reverse("post-list")
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

    def test_get_post(self, login_result: dict, post: dict):
        access_token = login_result["access_token"]
        auth_header = {"Authorization": "Bearer " + access_token}
        url = reverse("post-detail", kwargs={"pk": 1})
        client = Client()
        resp = client.get(
            path=url,
            headers=auth_header,
        )
        assert resp.status_code == 200
        logging.info(f"Message: {json.loads(resp.content)}")

    def test_view_post_list(self, login_result, posts: list):
        access_token = login_result["access_token"]
        auth_header = {"Authorization": "Bearer " + access_token}
        url = reverse("post-list")
        client = Client()
        for i in range(1, 3):
            resp = client.get(path=url, headers=auth_header, QUERY_STRING=f"page={i}")
            assert resp.status_code == 200
            logging.info(f"Message: {json.loads(resp.content)}")

    def test_put_post(self, login_result: dict, post: dict):
        access_token = login_result["access_token"]
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
        assert resp.status_code == 200
        logging.info(f"Message: {json.loads(resp.content)}")

    def test_delete_post(self, login_result: dict, post: dict):
        access_token = login_result["access_token"]
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
