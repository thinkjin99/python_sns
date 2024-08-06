from pydantic import BaseModel, Field


class ResponseValidator(BaseModel):
    message: str
    status: int = Field(default=200)
    data: dict | None = Field(default=None)
