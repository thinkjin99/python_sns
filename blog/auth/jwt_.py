import jwt
import datetime


from .validator import PayloadValidator


class JWT:
    algorithm = "HS256"
    secret = "kqxO+8QJcYPJuxshiZWHl1kVA+cLoGBA8TAtzYnmxe8="
    refresh_secret = "U83dtMRxSB2BjC0LVQgDiAsOqmVeUaKN3MpcbeSSEdc="

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
            secret = cls.refresh_secret
        else:
            exp = create_exp(datetime.timedelta(hours=3))
            secret = cls.secret

        payload.update({"exp": exp})
        payload_ = PayloadValidator(**payload)  # 원본 딕셔너리 수정에 위험이 있으므로
        token = jwt.encode(
            payload=payload_.model_dump(), key=secret, algorithm=cls.algorithm
        )
        return token

    @classmethod
    def decode(
        cls, token: str, verify_exp: bool = True, is_refresh: bool = False
    ) -> PayloadValidator:
        """
        JWT 토큰 디코딩

        Args:
            token (str): jwt 토큰

        Returns:
            dict | None: 토큰의 페이로드
        """

        secret = cls.refresh_secret if is_refresh else cls.secret
        data: dict = jwt.decode(
            token,
            secret,
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
