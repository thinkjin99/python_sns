import json
import logging
import pytest

from django.test import Client
from django.urls import reverse

from .fixtures import login_token, post, posts, basic_user, user2
from user.models import User
from .utils import login

logger = logging.getLogger("test")

TEST_USER_ID = "abc@naver.com"
TEST_USER_PASSWORD = "a123"
TEST_PROFILE_ID = "Test"


@pytest.mark.django_db
class TestPost:

    @pytest.fixture(autouse=True)
    def setup(self, basic_user):
        self.basic_user = basic_user
        self.login_token = login(self.basic_user)
        self.access_token = self.login_token["access_token"]

    def test_post_post(self):
        auth_header = {"Authorization": "Bearer " + self.access_token}
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

    def test_get_post(self, post):
        auth_header = {"Authorization": "Bearer " + self.access_token}
        url = reverse("post-detail", kwargs={"pk": 1})
        client = Client()
        resp = client.get(
            path=url,
            headers=auth_header,
        )
        assert resp.status_code == 200
        logging.info(f"Message: {json.loads(resp.content)}")

    def test_view_post_list(self, posts: list):
        auth_header = {"Authorization": "Bearer " + self.access_token}
        url = reverse("post-list")
        client = Client()
        for i in range(1, 3):
            resp = client.get(path=url, headers=auth_header, QUERY_STRING=f"page={i}")
            assert resp.status_code == 200
            logging.info(f"Message: {json.loads(resp.content)}")

    def test_put_post(self, post):
        auth_header = {"Authorization": "Bearer " + self.access_token}
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

    def test_delete_post(self, post):
        auth_header = {"Authorization": "Bearer " + self.access_token}
        url = reverse("post-detail", kwargs={"pk": 1})
        client = Client()
        resp = client.delete(
            path=url,
            headers=auth_header,
            content_type="application/json",
        )
        assert resp.status_code == 204
        logging.info(f"Message: Post successfully deleted")

    def test_non_author_delete(self, user2, post):
        login_token = login(user2)
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

    def test_non_author_put(self, user2, post):
        login_token = login(user2)
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
