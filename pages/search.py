from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

import settings
from base.locators import (
    GroupLocator,
    Locator,
)
from pages.base import OSFBasePage


class SearchPage(OSFBasePage):
    url = settings.OSF_HOME + '/search/'

    identity = Locator(By.CSS_SELECTOR, 'div[data-analytics-scope="Search page main"]')
    search_input = Locator(
        By.CSS_SELECTOR, '.ember-text-field.ember-view._search-input_fvrbco'
    )
    search_button = Locator(By.CSS_SELECTOR, 'button[data-test-search-submit]')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale')
    projects_tab_link = Locator(
        By.CSS_SELECTOR, 'a[data-test-topbar-object-type-link="Projects"]'
    )
    registrations_tab_link = Locator(
        By.CSS_SELECTOR, 'a[data-test-topbar-object-type-link="Registrations"]'
    )
    preprints_tab_link = Locator(
        By.CSS_SELECTOR, 'a[data-test-topbar-object-type-link="Preprints"]'
    )
    files_tab_link = Locator(
        By.CSS_SELECTOR, 'a[data-test-topbar-object-type-link="Files"]'
    )
    users_tab_link = Locator(
        By.CSS_SELECTOR, 'a[data-test-topbar-object-type-link="Users"]'
    )
    first_card_object_type_label = Locator(By.CSS_SELECTOR, 'div._type-label_qeqpmj')
    sort_by_button = Locator(
        By.CSS_SELECTOR,
        'div[data-test-topbar-sort-dropdown] > div.ember-view.ember-basic-dropdown-trigger.ember-power-select-trigger',
    )
    sort_by_date_newest = Locator(
        By.CSS_SELECTOR, '#ember-basic-dropdown-wormhole > div > ul > li:nth-child(2)'
    )

    # Group Locators
    search_results = GroupLocator(By.CSS_SELECTOR, '._result-card-container_qeqpmj')

    def get_first_non_withdrawn_registration(self):
        for result in self.search_results:
            try:
                result.find_element_by_class_name('_withdrawn-label_qeqpmj')
            except NoSuchElementException:
                return result.find_element_by_css_selector('div:nth-child(1) > h4 > a')
