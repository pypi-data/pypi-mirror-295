from gravybox.betterstack import collect_logger

logger = collect_logger()


class GravyboxException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.log_extras = {}


class BadStatusCode(GravyboxException):
    def __init__(self, response):
        message = "bad status code"
        super().__init__(message)
        self.response = response
        self.log_extras["status_code"] = response.status_code
        self.log_extras["payload"] = response.text


class DataUnavailable(GravyboxException):
    def __init__(self):
        message = "data is not available"
        super().__init__(message)


class UnexpectedCondition(GravyboxException):
    def __init__(self, condition):
        message = "encountered unexpected condition"
        super().__init__(message)
        self.log_extras["condition"] = condition
