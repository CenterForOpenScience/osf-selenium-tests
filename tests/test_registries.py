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

class TestRegistriesDiscoverPage:
    @markers.smoke_test
    @markers.core_functionality
    def test_search_results_exist(self, driver, landing_page):
        landing_page.search_box.send_keys_deliberately('QA Test\n')
        discover_page = RegistriesDiscoverPage(driver, verify=True)
        discover_page.loading_indicator.here_then_gone()
        assert len(discover_page.search_results) > 0

    @markers.core_functionality
    def test_detail_page(self, driver):
        """Test a registration detail page by grabbing the first search result from the discover page.
        """
        discover_page = RegistriesDiscoverPage(driver)
        discover_page.goto()
        discover_page.loading_indicator.here_then_gone()
        search_results = discover_page.search_results
        assert search_results

        discover_page.scroll_into_view(discover_page.osf_filter.element)
        discover_page.osf_filter.click()
        discover_page.loading_indicator.here_then_gone()

        target_registration = discover_page.get_first_non_withdrawn_registration()
        target_registration_title = target_registration.text
        target_registration.click()
        detail_page = RegistrationDetailPage(driver)
        detail_page.identity.present()
        assert RegistrationDetailPage(driver, verify=True)
        assert detail_page.identity.text in target_registration_title
