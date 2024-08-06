from django.http import JsonResponse
from response.validator import ResponseValidator


class JSONResponseMiddleWare:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def serialize(self, resp: ResponseValidator) -> dict:
        data = resp.model_dump()
        data.pop("status")
        return data

    def __call__(self, reqeust):
        resp = self.get_response(reqeust)
        if isinstance(resp, JsonResponse):
            return resp
        else:
            return JsonResponse(data=self.serialize(resp), status=resp.status)

    def process_exception(self, request, exception):
        try:
            resp: ResponseValidator = exception.resp
            return JsonResponse(data=self.serialize(resp), status=resp.status)

        except Exception as e:
            return JsonResponse(data="Server Error", status=500)
