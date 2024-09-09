def success(data):
    return BaseResponse(0, "success", data)


def failure(code, message):
    return BaseResponse(code, message, None)


class BaseResponse:
    def __init__(self, code: int, message: str, data: object):
        self.code = code
        self.message = message
        self.data = data
