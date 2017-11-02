class PageException(Exception):
    pass


class HttpError(PageException):
    def __init__(self, driver, code=None, error_info=None):
        self.driver = driver
        self.code = int(code)
        self.error_info = error_info
