import pytest
from django.test import Client
from django.urls import reverse

from user.models import User
from post.models import Post
from comment.models import Comment


TEST_USER_NAME = "abc@naver.com"
TEST_USER_PASSWORD = "a123"
TEST_PROFILE_ID = "Test"
TEST_USER_ID = 1
TEST_POST_ID = 1


@pytest.fixture
def basic_user():
    data = {
        "email": TEST_USER_NAME,
        "password": TEST_USER_PASSWORD,
        "profile_id": TEST_PROFILE_ID,
    }
    # if hasattr(User.objects,"create_user"):
    user = User.objects.create_user(**data)
    user.password = TEST_USER_PASSWORD
    user.follows.add(user)
    return user


@pytest.fixture
def user2():
    data = {
        "email": "test123@gmail.com",
        "password": "abc1234",
        "profile_id": "test2",
    }
    user = User.objects.create_user(**data)
    user.password = "abc1234"
    user.follows.add(user)
    return user


@pytest.fixture
def login_token() -> str:
    data = {
        "email": TEST_USER_NAME,
        "password": TEST_USER_PASSWORD,
        "profile_id": TEST_PROFILE_ID,
    }
    user = User.objects.create_user(**data)
    user.follows.add(user)

    url = reverse("user:login")
    data = {"email": TEST_USER_NAME, "password": TEST_USER_PASSWORD}
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
def post():
    post_data = {
        "title": "게시글 안녕하세요",
        "content": "나는 손범수",
        "author_id": TEST_USER_ID,
    }
    post = Post.objects.create(**post_data)
    return post


@pytest.fixture
def comment():
    comment_data = {
        "author_id": TEST_USER_ID,
        "post_id": TEST_POST_ID,
        "content": "코멘트 입니다",
    }
    comment = Comment()
    comment.objects.create(**comment_data)
    return comment


@pytest.fixture
def comments() -> list:
    comment_data = {
        "author_id": TEST_USER_ID,
        "post_id": TEST_POST_ID,
        "content": "코멘트 입니다",
    }
    comments = []
    comment = Comment()
    for i in range(20):
        copy = comment_data.copy()
        copy["content"] = f"코멘트 입니다 {i}"
        comment = Comment.objects.create(**copy)
        comments.append(comment)

    return comments


@pytest.fixture
def posts() -> list:
    post_data = {
        "title": "게시글 안녕하세요",
        "content": "나는 손범수",
        "author_id": TEST_USER_ID,
    }
    posts = []
    for i in range(20):
        copy = post_data.copy()
        copy["content"] = f"나는 손범수 {i}"
        post = Post.objects.create(**copy)
        posts.append(post)
    return posts


@pytest.fixture
def comment():
    comment_data = {
        "author_id": TEST_USER_ID,
        "post_id": TEST_POST_ID,
        "content": "코멘트 입니다",
    }
    comment = Comment.objects.create(**comment_data)
    return comment


@pytest.fixture
def comments() -> list:
    comment_data = {
        "author_id": TEST_USER_ID,
        "post_id": TEST_POST_ID,
        "content": "코멘트 입니다",
    }
    comments = []
    for i in range(20):
        copy = comment_data.copy()
        copy["content"] = f"코멘트 입니다 {i}"
        comment = Comment.objects.create(**copy)
        comments.append(comment)

    return comments
