import pytest
import markers
import settings
from pages.institutions import InstitutionsLandingPage, InstitutionBrandedPage

class TestInstitutionsPage:

    @pytest.fixture()
    def landing_page(self, driver):
        landing_page = InstitutionsLandingPage(driver)
        landing_page.goto()
        return landing_page

    def test_select_institution(self, driver, landing_page):
        landing_page.institution_list[0].click()
        assert InstitutionBrandedPage(driver, verify=True)

    def test_filter_by_institution(self, driver, landing_page, institution='Center For Open Science'):
        landing_page.search_bar.send_keys(institution)
        assert institution in landing_page.institution_list[0].text


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
