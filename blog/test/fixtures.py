import pytest
from django.test import Client
from django.urls import reverse

from user.models import User
from post.models import Post


TEST_USER_ID = "abc@naver.com"
TEST_USER_PASSWORD = "a123"
TEST_USER_DB_ID = 1


@pytest.fixture
def user() -> dict:
    data = {"email": "abc@naver.com", "password": "a123", "profile_id": "a123"}
    user = User.objects.create_user(**data)
    user.follows.add(user)
    return data


@pytest.fixture
def login_result(user) -> str:
    url = reverse("user:login")
    data = {"email": TEST_USER_ID, "password": TEST_USER_PASSWORD}
    client = Client()
    response = client.post(
        path=url,
        data=data,
    )
    # logging.info(f"header: {response.headers} data: {response.json()}")
    assert response.status_code == 200

    data = response.json()

    return data


@pytest.fixture
def post() -> dict:
    post_data = {
        "title": "안녕하세요",
        "content": "나는 손범수",
        "author_id": TEST_USER_DB_ID,
    }
    post = Post.objects.create(**post_data)
    return post.to_dict()


@pytest.fixture
def posts() -> list:
    post_data = {
        "title": "안녕하세요",
        "content": "나는 손범수",
        "author_id": TEST_USER_DB_ID,
    }
    posts = []
    for i in range(20):
        copy = post_data.copy()
        copy["content"] = f"나는 손범수 {i}"
        post = Post.objects.create(**copy)
        posts.append(post)
    return posts
