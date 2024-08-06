from pydantic import BaseModel, Field


class PayloadValidator(BaseModel):
    id: int
    exp: float = Field(frozen=True)
