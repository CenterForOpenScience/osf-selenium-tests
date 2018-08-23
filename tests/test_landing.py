import markers

from pages.landing import LandingPage


class TestLandingPage:

    @markers.core_functionality
    def test_loads(self, driver):
        landing_page = LandingPage(driver)
        landing_page.goto()
