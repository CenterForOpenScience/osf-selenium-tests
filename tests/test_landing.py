import pytest
import markers

from pages.landing import LandingPage, RegisteredReportsLandingPage

@pytest.fixture()
def landing_page(driver):
    landing_page = LandingPage(driver)
    landing_page.goto()
    return landing_page


class TestHomeLandingPage:

    @pytest.fixture()
    def page(self, landing_page):
        return landing_page

    @markers.core_functionality
    def test_landing_page(self, driver):
        LandingPage(driver, verify=True)

    #TO DO: Come back later and add other tests for elements on OSF Home page - see ENG-826


class TestRegisteredReportsLandingPage:

    @markers.core_functionality
    def test_landing_page(self, driver):
        landing_page = RegisteredReportsLandingPage(driver)
        landing_page.goto()
