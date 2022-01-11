from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

import settings
from base.locators import (
    ComponentLocator,
    GroupLocator,
    Locator,
)
from components.navbars import RegistriesNavbar
from pages.base import (
    GuidBasePage,
    OSFBasePage,
)


class BaseRegistriesPage(OSFBasePage):

    # Components
    navbar = ComponentLocator(RegistriesNavbar)


class RegistriesLandingPage(BaseRegistriesPage):
    url = settings.OSF_HOME + '/registries'

    identity = Locator(
        By.CSS_SELECTOR, '._RegistriesHeader_3zbd8x', settings.LONG_TIMEOUT
    )
    search_box = Locator(By.ID, 'search')


class RegistriesDiscoverPage(BaseRegistriesPage):
    url = settings.OSF_HOME + '/registries/discover'

    identity = Locator(
        By.CSS_SELECTOR, 'div[data-analytics-scope="Registries Discover page"]'
    )
    search_box = Locator(By.ID, 'search')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale', settings.LONG_TIMEOUT)
    osf_filter = Locator(
        By.CSS_SELECTOR, '[data-test-source-filter-id$="OSF Registries"]'
    )

    # Group Locators
    search_results = GroupLocator(
        By.CSS_SELECTOR, '._RegistriesSearchResult__Title_1wvii8'
    )

    def get_first_non_withdrawn_registration(self):
        for result in self.search_results:
            try:
                result.find_element_by_class_name('label-default')
            except NoSuchElementException:
                return result.find_element_by_css_selector(
                    '[data-test-result-title-id]'
                )


class RegistrationDetailPage(GuidBasePage):
    identity = Locator(By.CSS_SELECTOR, '[data-test-registration-title]')


class RegistrationAddNewPage(BaseRegistriesPage):
    url = settings.OSF_HOME + '/registries/osf/new'
    identity = Locator(By.CSS_SELECTOR, 'form[data-test-new-registration-form]', settings.LONG_TIMEOUT)

    # validate add new page
    add_new_main_wormhole = Locator(By.ID, 'div[ember-basic-dropdown-wormhole]', settings.LONG_TIMEOUT)
    dropdown_wormhole = Locator(By.XPATH, '//div[@id=‘ember-basic-dropdown-wormhole’]', settings.LONG_TIMEOUT) # this one works

    # has project
    has_project_button = Locator(By.XPATH, '//body//main[1]//div[2]//div[1]/div[1]//form[1]//div[1]//fieldset[1]//div[1]')
    # has_project_button = Locator(By.CSS_SELECTOR, 'form > div > fieldset > div:nth-child(2)')

    # no project
    no_project_button  = Locator(By.XPATH, '//div[@id="ember44"]//form[@class="_registrationForm_1p1l4a"]//div[1]//fieldset[1]//div[2]//input[1]')
    # has_project_button = Locator(By.CSS_SELECTOR, 'form > div > fieldset > div:nth-child(2)')

    # project_selection
    project_selection_dropdown = Locator(By.XPATH, '//body//main[1]//div[2]//div[1]/div[1]//form[1]//label[1]//div[1]//span[1]')
    first_project_selection = Locator(By.XPATH, '//body//div[3]//div[1]//ul[1]//li[1]')
    second_project_selection =  Locator(By.XPATH, '//body//div[3]//div[1]//ul[1]//li[2]')

    # select schema type
    schema_type_dropdown = Locator(By.XPATH, '//body//main[1]//div[2]//div[1]/div[1]//form[1]//label[2]//div[1]//span[1]')
    preregistration_schema_selection = Locator(By.XPATH, '//body//div[3]//div[1]//ul[1]//li[4]')
    add_new_submit_button = Locator(By.CSS_SELECTOR, 'button[data-test-start-registration-button]')


class RegistrationDraftPage(BaseRegistriesPage):
    identity = Locator(By.CSS_SELECTOR, 'nav[data-test-side-nav]', settings.LONG_TIMEOUT)

    registration_title_input = Locator(By.XPATH, '//input["ember-text-field"][1]')

    registration_description_input = Locator(By.XPATH, '//form[1]//textarea[1]')

    add_contributor_plus_button = Locator(By.XPATH, '//form[1]//div[3]//button[1]')

    add_contributor_search_box = Locator(By.XPATH, '//form[1]//div[4]//input[1]')

    add_contributor_search_button = Locator(By.XPATH, '//form[1]//div[4]//button[1]')

    add_first_contributor_result = GroupLocator(By.XPATH, '//form[1]//div["data-test-user-search-results"][4]//div[2]//div[3]//div[1]//span[4]//button[1]')

    remove_contributor_button_first_el = Locator(By.XPATH, 'button[data-test-start-registration-button]') # for use with method to first clear all contributors

    category_power_select = Locator(By.XPATH, '//form[1]//div[6]//div[1]')

    # TODO fill in other dropdown tags for data, other, software, analysis, procedure, and hypothesis
    category_analysis_dropdown_select = Locator(By.XPATH, '//ul[@class="ember-power-select-options"]//li[@class="ember-power-select-option"]//span[text()="Analysis"]//parent::span//parent::li')

    license_power_select = Locator(By.XPATH, '//form[1]//div[8]//div[1]//div[1]//div[@role="button"]')

    # CC-By Attribution 4.0 International
    license_cc_international_select = Locator(By.XPATH, '//ul[@class="ember-power-select-options"]//li[@class="ember-power-select-option"]//span[text()="CC-By Attribution 4.0 International"]')

    subject_engineering_checkbox = Locator(By.XPATH, '//label[text()="Engineering"]')

    tags_input = Locator(By.XPATH, '//li[@class="emberTagInput-new"]//input[@aria-label="Add a tag to enhance discoverability"]')

    draft_registration_next_button = Locator(By.XPATH, '//button[text()="Next"]')

    # no_data_collected_radio_button = Locator(By.XPATH, '//main//fieldset//div[1]//div[1]//div[1]//div[1]//input[1]')
    no_data_collected_radio_button = Locator(By.XPATH, '//input[@value="No, data collection has not begun"]')

    # data_collected_radio_button = Locator(By.XPATH, '//main//fieldset//div[1]//div[1]//div[1]//div[2]//input[1]')
    data_collected_radio_button = Locator(By.XPATH, '//input[@value="Yes, data collection is underway or complete"]')

    # data_looked_at_radio_button = Locator(By.XPATH, '//main//fieldset[2]//div[1]//div[1]//div[1]//div[1]//input[1]')
    data_looked_at_radio_button = Locator(By.XPATH, '//input[@value="Yes"]')

    # data_not_looked_at_radio_button = Locator(By.XPATH, '//main//fieldset[2]//div[1]//div[1]//div[1]//div[2]//input[1]')
    data_not_looked_at_radio_button = Locator(By.XPATH, '//input[@value="No"]')

    comments_textarea = Locator(By.XPATH, '//textarea[1]')

    draft_review_button = Locator(By.XPATH, '//button[text()="Review"]')

    make_registration_public_radio = Locator(By.XPATH, '//input[@value="immediate"]')

    make_registration_embargo_radio = Locator(By.XPATH, '//input[@value="//input[@value="embargo"]')

    demo_back_button = Locator(By.XPATH, '//button[text()="Submit"]//following-sibling::button[text()="Back"]')

    register_draft_button = Locator(By.XPATH, '//button[text()="Register"]')

    submit_draft_button = Locator(By.XPATH, '//button[text()="Submit"]')

class MyRegistrationsPage(BaseRegistriesPage):
    identity = Locator(By.CSS_SELECTOR, '[]')
