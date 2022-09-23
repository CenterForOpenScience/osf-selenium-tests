import pytest
from selenium.webdriver.common.keys import Keys

import markers
import settings
from api import osf_api
from pages.registries import (
    RegistrationDetailPage,
    RegistriesDiscoverPage,
    RegistriesLandingPage,
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
        landing_page.search_box.send_keys_deliberately('QA Test')
        landing_page.search_box.send_keys(Keys.ENTER)
        discover_page = RegistriesDiscoverPage(driver, verify=True)
        discover_page.loading_indicator.here_then_gone()
        assert len(discover_page.search_results) > 0

    @markers.smoke_test
    @markers.core_functionality
    def test_detail_page(self, driver):
        """Test a registration detail page by grabbing the first search result from the discover page."""
        discover_page = RegistriesDiscoverPage(driver)
        discover_page.goto()
        if not settings.PRODUCTION:
            # Since all of the testing environments use the same SHARE server, we need to enter a value in the search
            # input box that will ensure that the results are specific to the current environment.  We can do this by
            # searching for the test environment in the affiliations metadata field.  The affiliated institutions as
            # setup in the testing environments typically include the specific environment in their names.
            # EX: The Center For Open Science [Stage2]
            if settings.STAGE1:
                # need to drop the 1 since they usually just use 'Stage' instead of 'Stage1'
                environment = 'stage'
            else:
                environment = settings.DOMAIN
            search_text = 'affiliations:' + environment
            discover_page.search_box.send_keys_deliberately(search_text)
            discover_page.search_box.send_keys(Keys.ENTER)
        discover_page.loading_indicator.here_then_gone()
        search_results = discover_page.search_results
        assert search_results

        target_registration = discover_page.get_first_non_withdrawn_registration()
        target_registration_title = target_registration.text
        target_registration.click()
        detail_page = RegistrationDetailPage(driver)
        detail_page.identity.present()
        assert RegistrationDetailPage(driver, verify=True)
        assert detail_page.identity.text in target_registration_title


@markers.smoke_test
@markers.core_functionality
class TestBrandedRegistriesPages:
    def providers():
        """Return all registration providers."""
        return osf_api.get_providers_list(type='registrations')

    @pytest.fixture(params=providers(), ids=[prov['id'] for prov in providers()])
    def provider(self, request):
        return request.param

    def test_discover_page(self, session, driver, provider):
        """This test will load the Discover page for each Branded Registry Provider that
        exists in an environment.
        """
        if provider['attributes']['branded_discovery_page']:
            discover_page = RegistriesDiscoverPage(driver, provider=provider)
            discover_page.goto()
            discover_page.loading_indicator.here_then_gone()
            assert RegistriesDiscoverPage(driver, verify=True)
