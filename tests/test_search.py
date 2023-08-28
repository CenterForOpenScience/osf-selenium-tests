import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import markers
from pages.search import SearchPage


@pytest.fixture()
def search_page(driver):
    search_page = SearchPage(driver)
    search_page.goto()
    return search_page


class TestSearchPage:
    @markers.smoke_test
    @markers.core_functionality
    def test_search_results_exist_all_tab(self, driver, search_page):
        search_page.search_input.send_keys('test')
        search_page.search_input.send_keys(Keys.ENTER)
        search_page.loading_indicator.here_then_gone()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'div[data-test-search-result-card]')
            )
        )
        assert len(search_page.search_results) > 0

    def test_search_results_exist_projects_tab(self, driver, search_page):
        search_page.search_input.send_keys('test')
        search_page.search_input.send_keys(Keys.ENTER)
        search_page.loading_indicator.here_then_gone()
        # Switch to the Projects Tab
        search_page.projects_tab_link.click()
        search_page.loading_indicator.here_then_gone()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'div[data-test-search-result-card]')
            )
        )
        assert len(search_page.search_results) > 0
        # Verify that first search result is of Project type
        assert search_page.first_card_object_type_label.text[:7] == 'PROJECT'

    def test_search_results_exist_registrations_tab(self, driver, search_page):
        search_page.search_input.send_keys('test')
        search_page.search_input.send_keys(Keys.ENTER)
        search_page.loading_indicator.here_then_gone()
        # Switch to the Registrations Tab
        search_page.registrations_tab_link.click()
        search_page.loading_indicator.here_then_gone()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'div[data-test-search-result-card]')
            )
        )
        assert len(search_page.search_results) > 0
        # Verify that first search result is of Registration type
        assert search_page.first_card_object_type_label.text[:12] == 'REGISTRATION'

    def test_search_results_exist_preprints_tab(self, driver, search_page):
        search_page.search_input.send_keys('test')
        search_page.search_input.send_keys(Keys.ENTER)
        search_page.loading_indicator.here_then_gone()
        # Switch to the Preprints Tab
        search_page.preprints_tab_link.click()
        search_page.loading_indicator.here_then_gone()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'div[data-test-search-result-card]')
            )
        )
        assert len(search_page.search_results) > 0
        # Verify that first search result is of Preprint type
        assert search_page.first_card_object_type_label.text == 'PREPRINT'

    def test_search_results_exist_files_tab(self, driver, search_page):
        search_page.search_input.send_keys('test')
        search_page.search_input.send_keys(Keys.ENTER)
        search_page.loading_indicator.here_then_gone()
        # Switch to the Files Tab
        search_page.files_tab_link.click()
        search_page.loading_indicator.here_then_gone()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'div[data-test-search-result-card]')
            )
        )
        assert len(search_page.search_results) > 0
        # Verify that first search result is of File type
        assert search_page.first_card_object_type_label.text == 'FILE'

    def test_search_results_exist_users_tab(self, driver, search_page):
        search_page.loading_indicator.here_then_gone()
        # Switch to the Users Tab
        search_page.users_tab_link.click()
        search_page.loading_indicator.here_then_gone()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'div[data-test-search-result-card]')
            )
        )
        assert len(search_page.search_results) > 0
        # Verify that first search result is of User type
        assert search_page.first_card_object_type_label.text == 'USER'
