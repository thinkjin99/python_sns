import jwt
import pathlib
import datetime


from .validator import PayloadValidator


PATH = pathlib.Path("/Users/jin/Programming/blog/blog/user")


def read_pem_key(path: str | pathlib.Path) -> str:
    with open(path) as f:
        secret = f.read(2048)
        return secret


class JWT:
    # def __init__(self) -> None:
    algorithm = "HS256"
    # self.public = read_pem_key(PATH.joinpath("public_key.pem"))
    secret = read_pem_key(PATH.joinpath("private_key.pem"))

    @classmethod
    def encode(cls, payload: dict) -> str:
        """
        RS256 알고리즘으로 토큰을 인코딩 합니다.

        Args:
            payload (dict): json 토큰에 포함할 데이터

        Returns:
            str: JWT 토큰
        """
        create_exp = lambda x: datetime.datetime.timestamp(datetime.datetime.now() + x)

        if payload.get("is_refresh"):
            exp = create_exp(datetime.timedelta(days=60))
        else:
            exp = create_exp(datetime.timedelta(hours=3))

        payload.update({"exp": exp})
        payload_ = PayloadValidator(**payload)  # 원본 딕셔너리 수정에 위험이 있으므로
        token = jwt.encode(
            payload=payload_.model_dump(), key=cls.secret, algorithm=cls.algorithm
        )
        return token

    @classmethod
    def decode(cls, token: str, verify_exp: bool = True) -> PayloadValidator:
        """
        JWT 토큰 디코딩

        Args:
            token (str): jwt 토큰

        Returns:
            dict | None: 토큰의 페이로드
        """
        data: dict = jwt.decode(
            token,
            cls.secret,
            algorithms=[cls.algorithm],
            options={"verify_exp": verify_exp},
        )
        payload: PayloadValidator = PayloadValidator(**data)
        return payload


if __name__ == "__main__":
    my_jwt = JWT()
    token = my_jwt.encode({"user_id": 1})
    print(my_jwt.secret)
    print(my_jwt.decode(token))
