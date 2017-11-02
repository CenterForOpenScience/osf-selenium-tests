class PageException(Exception):
    pass


class HttpError(PageException):
    def __init__(self, driver, code=None):
        self.driver = driver
        self.code = int(code)


class LoginError(PageException):
    def __init__(self, driver, error_info=None):
        self.driver = driver
        self.error_info = error_info
