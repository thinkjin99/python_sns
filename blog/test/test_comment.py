import json
import logging
import pytest

from django.test import Client
from django.urls import reverse

from .fixtures import basic_user, post, posts, comments, comment
from user.models import User
from .utils import login

logger = logging.getLogger("test")

TEST_USER_ID = "abc@naver.com"
TEST_USER_PASSWORD = "a123"
TEST_PROFILE_ID = "Test"


@pytest.mark.django_db
class TestComment:
    @pytest.fixture(autouse=True)
    def setup(self, basic_user, post):
        self.basic_user = basic_user
        self.login_token = login(self.basic_user)
        self.access_token = self.login_token["access_token"]
        self.post = post

    def test_crate_comment(self):
        auth_header = {"Authorization": "Bearer " + self.access_token}
        comment_data = {"content": "나는 손범수", "post": self.post.id}
        url = reverse("comment-list")
        client = Client()

        for _ in range(5):
            resp = client.post(
                path=url,
                data=comment_data,
                content_type="application/json",
                headers=auth_header,
            )

            logging.info(f"Message: {json.loads(resp.content)}")
            assert resp.status_code == 201

    def test_get_comments_in_post(self, comments: list):
        auth_header = {"Authorization": "Bearer " + self.access_token}
        url = reverse("post-comment", kwargs={"post_id": self.post.id})
        client = Client()
        resp = client.get(
            path=url,
            headers=auth_header,
        )
        assert resp.status_code == 200
        logging.info(f"Message: {json.loads(resp.content)}")

    def test_get_comment_list(self):
        auth_header = {"Authorization": "Bearer " + self.access_token}
        url = reverse("comment-list")
        client = Client()
        resp = client.get(path=url, headers=auth_header)
        assert resp.status_code == 400
        logging.info(f"Message: {json.loads(resp.content)}")

    def test_get_comment(self, comment):
        auth_header = {"Authorization": "Bearer " + self.access_token}
        url = reverse("comment-detail", kwargs={"pk": comment.id})
        client = Client()
        resp = client.get(path=url, headers=auth_header)
        assert resp.status_code == 200
        logging.info(f"Message: {json.loads(resp.content)}")

    def test_put_comment(self, comment):
        auth_header = {"Authorization": "Bearer " + self.access_token}
        url = reverse("comment-detail", kwargs={"pk": comment.id})
        client = Client()
        comment_data = {"content": "나는 손범수222", "post": self.post.id}

        resp = client.put(
            path=url,
            headers=auth_header,
            data=comment_data,
            content_type="application/json",
        )
        assert resp.status_code == 200
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

    # def test_non_author_delete(self, login_token, post):
    #     username = "test123@gmail.com"
    #     password = "abc1234"
    #     profile_id = "test1"
    #     user = create_user(username, password, profile_id)
    #     login_token = login(username, password)
    #     access_token = login_token["access_token"]
    #     auth_header = {"Authorization": "Bearer " + access_token}
    #     url = reverse("post-detail", kwargs={"pk": 1})
    #     client = Client()
    #     resp = client.delete(
    #         path=url,
    #         headers=auth_header,
    #         content_type="application/json",
    #     )
    #     assert resp.status_code == 403
    #     logging.info(f"Message: Correctly denied")

    # def test_non_author_put(self, login_token, post):
    #     username = "test123@gmail.com"
    #     password = "abc1234"
    #     profile_id = "test1"
    #     user = create_user(username, password, profile_id)
    #     login_token = login(username, password)
    #     access_token = login_token["access_token"]
    #     auth_header = {"Authorization": "Bearer " + access_token}
    #     url = reverse("post-detail", kwargs={"pk": 1})
    #     client = Client()
    #     post_data = {
    #         "title": "안녕하세요",
    #         "content": "나는 손범수22",
    #     }
    #     resp = client.put(
    #         path=url,
    #         data=post_data,
    #         headers=auth_header,
    #         content_type="application/json",
    #     )
    #     assert resp.status_code == 403
    #     logging.info(f"Message: Correctly denied")
