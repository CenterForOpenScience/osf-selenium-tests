import pytest
import markers

from tests.generic import CreateUserMixin
from pages.landing import LandingPage, RegisteredReportsLandingPage

@pytest.fixture()
def landing_page(driver):
    landing_page = LandingPage(driver)
    landing_page.goto()
    return landing_page


class TestLandingPage(CreateUserMixin):

    @pytest.fixture()
    def page(self, landing_page):
        return landing_page


class TestRegisteredReportsLandingPage:

    @markers.core_functionality
    def test_landing_page(self, driver):
        landing_page = RegisteredReportsLandingPage(driver)
        landing_page.goto()
