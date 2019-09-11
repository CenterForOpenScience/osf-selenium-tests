import pytest

from tests.generic import CreateUserMixin
from pages.register import RegisterPage

@pytest.fixture()
def register_page(driver):
    register_page = RegisterPage(driver)
    register_page.goto()
    return register_page


class TestRegisterPage(CreateUserMixin):

    @pytest.fixture()
    def page(self, register_page):
        return register_page
