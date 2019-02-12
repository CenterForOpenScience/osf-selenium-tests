import pytest

import markers
import settings
from pages.institutions import InstitutionsLandingPage, InstitutionBrandedPage

class TestInstitutionsPage:

    def test_institutions_page_loads(self, driver):
        landing_page = InstitutionsLandingPage(driver)
        landing_page.goto()

class TestCustomDomains:

    @markers.smoke_test
    @pytest.mark.parametrize('domain', settings.CUSTOM_INSTITUTION_DOMAINS)
    def test_arrive_at_myprojects_page(self, driver, domain):
        """Test custom institutional domains. Skipped on any server that has no custom domains
        """
        #TODO: Add check for institution name
        driver.get(domain)
        InstitutionBrandedPage(driver, verify=True)
        assert domain in driver.current_url
