from typing_extensions import Annotated
from pydantic import BaseModel, StringConstraints, field_validator
from user.models import User


class PostValidator(BaseModel):
    title: Annotated[
        str,
        StringConstraints(
            pattern=r"^[a-zA-Zㄱ-ㅎ가-힣0-9!~.,\s]+$",
            max_length=50,
        ),
    ]
    content: Annotated[
        str,
        StringConstraints(
            pattern=r"^[a-zA-Zㄱ-ㅎ가-힣0-9!~.,\s]+$",
            max_length=500,
        ),
    ]
    author_id: int

    # @field_validator("author_id")
    # def check_user_exists(cls, author_id: int):
    #     try:
    #         User.objects.get(id=author_id)
    #         return author_id
    #     except User.DoesNotExist:
    #         raise ValueError("User is not exists")


