import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import markers
import settings
from pages.institutions import (
    InstitutionBrandedPage,
    InstitutionsLandingPage,
)


class TestInstitutionsPage:
    @pytest.fixture()
    def landing_page(self, driver):
        landing_page = InstitutionsLandingPage(driver)
        landing_page.goto()
        return landing_page

    def test_select_institution(self, driver, landing_page):
        landing_page.institution_list[0].click()
        assert InstitutionBrandedPage(driver, verify=True)

    def test_filter_by_institution(
        self, driver, landing_page, institution='Center For Open Science'
    ):
        landing_page.search_bar.send_keys(institution)
        assert institution in landing_page.institution_list[0].text


class TestCustomDomains:
    @markers.smoke_test
    @pytest.mark.parametrize('domain', settings.CUSTOM_INSTITUTION_DOMAINS)
    def test_arrive_at_myprojects_page(self, driver, domain):
        """Test custom institutional domains. Skipped on any server that has no custom domains"""
        # TODO: Add check for institution name
        driver.get(domain)
        institution_page = InstitutionBrandedPage(driver, verify=True)
        assert domain in driver.current_url
        # first check if the collection is empty - this may often be the case in the test environments
        if institution_page.empty_collection_indicator.absent():
            # wait for projects table to start loading and verify that there are some projects listed
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#tb-tbody > div > div > div.tb-row')
                )
            )
            # projects are loaded in batches in varying sizes - anywhere from 4 to 15 at a time
            assert len(institution_page.project_list) >= 4
