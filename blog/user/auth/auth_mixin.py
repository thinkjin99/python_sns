from django.views import View
from django.http import HttpRequest

from .validator import PayloadValidator
from .jwt_ import JWT
from response.exceptions import UnAuthorizedException


class JWTRequiredView(View):
    def set_payload(self, payload: PayloadValidator):
        self.payload = payload

    def get_payload(self) -> PayloadValidator:
        return self.payload

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        auth_header: str = request.headers["Authorization"]
        protocol, _, token = auth_header.partition(" ")
        if protocol.lower() != "bearer":
            raise UnAuthorizedException

        jwt = JWT()
        if payload := jwt.decode(token):
            self.set_payload(payload)
        else:
            raise UnAuthorizedException

        return super().dispatch(request, *args, **kwargs)  # dispatch from View
