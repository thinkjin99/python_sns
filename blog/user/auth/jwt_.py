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
    def __init__(self) -> None:
        self.algorithm = "RS256"
        self.public = read_pem_key(PATH.joinpath("public_key.pem"))
        self.secret = read_pem_key(PATH.joinpath("private_key.pem"))
        self.payload = None

    def valid_auth(self, request) -> str:
        """
        토큰 검증 함수

        Args:
            request (_type_): HTTP 리퀘스트 데이터

        Returns:
            str: Authenication 헤더 토큰 정보
        """
        authorization = request.headers.get("Authorization")
        assert (
            authorization
        ), "No Authorization header"  # bearer 등의 암호 프로토콜 제공 안할 경우 오류
        scheme, _, token = authorization.partition(" ")
        assert scheme != "bearer", "Only use Bearer token"
        return token

    def encode(self, payload: dict) -> str:
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
            payload=payload_.model_dump(), key=self.secret, algorithm=self.algorithm
        )
        return token

    def decode(self, token: str, verify_exp: bool = True) -> PayloadValidator | None:
        """
        JWT 토큰 디코딩

        Args:
            token (str): jwt 토큰

        Returns:
            dict | None: 토큰의 페이로드
        """
        try:
            data: dict = jwt.decode(
                token,
                self.public,
                algorithms=[self.algorithm],
                options={"verify_exp": verify_exp},
            )
            payload: PayloadValidator = PayloadValidator(**data)
            return payload

        except jwt.exceptions.ExpiredSignatureError as e:
            return None  # TODO Add logging


if __name__ == "__main__":
    my_jwt = JWT()
    token = my_jwt.encode({"user_id": 1})
    print(my_jwt.secret)
    print(my_jwt.decode(token))
