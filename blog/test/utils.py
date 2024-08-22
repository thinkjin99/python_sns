from django.test import Client
from django.urls import reverse

from user.models import User


def login(user: User):
    url = reverse("user:login")
    data = {"email": user.email, "password": user.password}
    client = Client()
    response = client.post(
        path=url,
        data=data,
    )
    # logging.info(f"header: {response.headers} data: {response.json()}")
    assert response.status_code == 200
    data = response.json()
    return data
