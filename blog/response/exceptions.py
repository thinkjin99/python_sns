from response.validator import ResponseValidator


class UnAuthorizedException(Exception):
    def __init__(self, *args, **kwargs) -> None:
        self.resp = ResponseValidator(message="Invalid Token", status=401)
        super().__init__(*args, **kwargs)


class UnProcessableException(Exception):
    def __init__(self, *args, **kwargs) -> None:
        self.resp = ResponseValidator(message="Invalid Data", status=422)
        super().__init__(*args, **kwargs)


class NotFoundException(Exception):
    def __init__(self, *args: object) -> None:
        self.resp = ResponseValidator(message="Resource Not Founded", status=404)
        super().__init__(*args)
