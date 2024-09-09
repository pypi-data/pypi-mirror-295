from enum import Enum


class ErrorCode(Enum):
    SYSTEM_ERROR = (-2, "python容器系统错误")
    BUSINESS_ERROR = (100000, "业务异常")
    CAN_NOT_FIND_CRAWLER = (100001, "can't find the crawler")
    IP_BLOCK_ERROR = (100002, "ip block error")
    NO_RETRY_ERROR = (100003, "no retry error")

    def __init__(self, code, message):
        self._code = code
        self._message = message

    @property
    def code(self):
        return self._code

    @property
    def message(self):
        return self._message
