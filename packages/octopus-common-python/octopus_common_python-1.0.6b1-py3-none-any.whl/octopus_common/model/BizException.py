from octopus_common.enums.ErrorCode import ErrorCode
from octopus_common.model.ResultDetail import ResultDetail


class BizException(Exception):
    errorCode = ErrorCode.BUSINESS_ERROR.code
    message = ErrorCode.BUSINESS_ERROR.message

    def __init__(self, error_code: ErrorCode = ErrorCode.BUSINESS_ERROR):
        self.errorCode = error_code.code
        self.message = error_code.message


class CrawlerException(BizException, ResultDetail):
    classType = "com.ctrip.fx.octopus.crawler.CrawlerException"

    def __init__(self, code: int = ErrorCode.BUSINESS_ERROR.code,
                 message: str = ErrorCode.BUSINESS_ERROR.message):
        self.errorCode = code
        self.message = message


class IpBlockException(BizException, ResultDetail):
    classType = "com.ctrip.fx.octopus.crawler.IPBlockException"

    def __init__(self, code: int = ErrorCode.IP_BLOCK_ERROR.code,
                 message: str = ErrorCode.IP_BLOCK_ERROR.message):
        self.errorCode = code
        self.message = message


class NoRetryException(BizException, ResultDetail):
    classType = "com.ctrip.fx.octopus.crawler.NoRetryException"

    def __init__(self):
        self.code = ErrorCode.NO_RETRY_ERROR.code
        self.message = ErrorCode.NO_RETRY_ERROR.message
