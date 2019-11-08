import pytest
import markers

from tests.generic import CreateUserMixin
from pages.landing import LandingPage, RegisteredReportsLandingPage

@pytest.fixture()
def landing_page(driver):
    landing_page = LandingPage(driver)
    landing_page.goto()
    return landing_page

class TestLandingPageUserCreation(CreateUserMixin):

    @pytest.fixture()
    def page(self, landing_page):
        return landing_page

class TestLandingPage():

    @pytest.fixture()
    def page(self, landing_page):
        return landing_page

    def test_testimonial_carousel(self, page):
        assert page.testimonial_carousel.present()

# why does the test refresh multiple times?

"""
Click Get Started, confirm goes to correct page
Search? maybe, can use existing search test parts
Could maybe click Learn More, confrm goes to correct page
Testimonial carousel -- test carets??? test seeing someone's research?

"""
class TestRegisteredReportsLandingPage:

    @markers.core_functionality
    def test_landing_page(self, driver):
        landing_page = RegisteredReportsLandingPage(driver)
        landing_page.goto()
