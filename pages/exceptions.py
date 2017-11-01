class PageException(Exception):
    pass


class HttpError(PageException):
    def __init__(self, driver, code=None):
        self.driver = driver
        self.code = int(code)