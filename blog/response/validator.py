from pydantic import BaseModel, Field


def json_api(func):
    def wraaper(*args, **kwargs):
        response = ResponseValidator(message="success", status=200)
        status, data = func(*args, **kwargs)
        response.status = status
        response.data = data
        return response

    return wraaper


class ResponseValidator(BaseModel):
    message: str
    status: int = Field(default=200)
    data: dict | None = Field(default=None)

    def __init__(self, status: int, message: str, data: dict | None = None):
        super().__init__(status=status, message=message, data=data)

    @classmethod
    def created(cls, data):
        return cls(201, "created", data)

    @classmethod
    def success(cls, message: str = "success", data: dict | None = None):
        return cls(200, message, data)
