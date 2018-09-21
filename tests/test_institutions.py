import pytest

import markers
import settings
from pages.project import InstitutionsLandingPage


class TestCustomDomains:

    @markers.smoke_test
    @pytest.mark.parametrize('domain', settings.CUSTOM_INSTITUTION_DOMAINS)
    def test_arrive_at_myprojects_page(self, driver, domain):
        #TODO: Add check for institution name
        driver.get(domain)
        InstitutionsLandingPage(driver, verify=True)
