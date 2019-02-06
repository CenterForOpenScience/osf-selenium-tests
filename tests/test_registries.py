import pytest
import markers

from pages.registries import (
    RegistriesLandingPage,
    RegistriesDiscoverPage,
    RegistrationDetailPage
)

@pytest.fixture
def landing_page(driver):
    landing_page = RegistriesLandingPage(driver)
    landing_page.goto()
    return landing_page

class TestRegistriesLandingPage:
    @markers.smoke_test
    @markers.core_functionality
    def test_landing_page_loads(self, driver):
        RegistriesLandingPage(driver).goto()

class TestRegistriesDiscoverPage:

    @markers.core_functionality
    def test_discover_page_loads(self, driver):
        RegistriesDiscoverPage(driver).goto()

    @markers.smoke_test
    @markers.core_functionality
    def test_search_results_exist(self, driver, landing_page):
        landing_page.search_button.click()
        discover_page = RegistriesDiscoverPage(driver, verify=True)
        discover_page.loading_indicator.here_then_gone()
        assert len(discover_page.search_results) > 0

    def test_detail_page(self, driver):
        """Test a registration detail page by grabbing the first search result from the discover page.
        """
        discover_page = RegistriesDiscoverPage(driver)
        discover_page.goto()
        discover_page.loading_indicator.here_then_gone()
        search_results = discover_page.search_results
        assert search_results
        search_results[0].click()
        RegistrationDetailPage(driver, verify=True)
