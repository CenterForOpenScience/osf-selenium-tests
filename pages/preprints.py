import pytest
import settings

from urllib.parse import urljoin
from selenium.webdriver.common.by import By

from base.locators import Locator, ComponentLocator, GroupLocator
from components.navbars import PreprintsNavbar
from pages.base import OSFBasePage, GuidBasePage


class BasePreprintPage(OSFBasePage):
    """The base page from which all preprint pages inherit.
    """
    base_url = settings.OSF_HOME + '/preprints/'
    url_addition = ''
    navbar = ComponentLocator(PreprintsNavbar)

    def __init__(self, driver, verify=False, provider=None):
        self.provider = provider
        if provider:
            self.provider_id = provider['id']
            self.provider_name = provider['attributes']['name']
            self.provider_domain = provider['attributes']['domain']

        super().__init__(driver, verify)

    @property
    def url(self):
        """Set the URL based on the provider domain.
        """
        if self.provider and self.provider_id != 'osf':
            if self.provider['attributes']['domain_redirect_enabled']:
                return urljoin(self.provider_domain, self.url_addition)
            else:
                return urljoin(self.base_url, self.provider_id) + '/' + self.url_addition
        return self.base_url + self.url_addition

    def verify(self):
        """Return true if you are on the expected page.
        Checks both the general page identity and the branding.
        """
        if self.provider and self.provider_id != 'osf':
            return super().verify() and self.provider_name in self.navbar.title.text
        return super().verify()


class PreprintLandingPage(BasePreprintPage):
    identity = Locator(By.CSS_SELECTOR, '.ember-application .preprint-header', settings.LONG_TIMEOUT)
    add_preprint_button = Locator(By.CLASS_NAME, 'preprint-submit-button', settings.LONG_TIMEOUT)
    search_button = Locator(By.CSS_SELECTOR, '.preprint-search .btn-default')


class PreprintSubmitPage(BasePreprintPage):
    url_addition = 'submit'

    identity = Locator(By.CLASS_NAME, 'preprint-submit-header')
    select_a_service_save_button = Locator(By.CSS_SELECTOR, '#preprint-form-server button.btn.btn-primary')

    upload_new_preprint_button = Locator(By.CSS_SELECTOR, '#preprint-form-upload > div > div > div > div > div > div:nth-child(1) > button')
    upload_from_existing_project_button = Locator(By.CSS_SELECTOR, '#preprint-form-upload > div > div > div > div > div > div:nth-child(2) > button')
    upload_project_selector = Locator(By.CSS_SELECTOR, '#preprint-form-upload .ember-power-select-placeholder')
    upload_project_selector_input = Locator(By.CSS_SELECTOR, '#preprint-form-upload .ember-power-select-search-input')
    upload_project_help_text = Locator(By.CSS_SELECTOR, '.ember-power-select-option--search-message')
    upload_project_selector_project = Locator(By.CSS_SELECTOR, '.ember-power-select-option')
    upload_existing_project_new_file_button = Locator(By.CSS_SELECTOR, '#preprint-form-upload .fa-cloud-upload')
    upload_existing_file_button = Locator(By.CSS_SELECTOR, '#preprint-form-upload .fa-th-list')
    upload_select_file = Locator(By.CSS_SELECTOR, '.file-browser-item > a:nth-child(2)')
    create_new_component_button = Locator(By.CSS_SELECTOR, '#convertExistingOrCreateComponent .fa-plus-circle')
    convert_existing_component_button = Locator(By.CSS_SELECTOR, '#convertExistingOrCreateComponent .fa-cube')
    continue_with_this_project_button = Locator(By.CSS_SELECTOR, '.upload-section-block .btn-success')
    create_new_component = Locator(By.CSS_SELECTOR, '.upload-section-block .btn-default')
    upload_save_button = Locator(By.CSS_SELECTOR, '.upload-section-block.ember-view.preprint-form-section.cp-Panel.cp-is-open > div > div > button')

    first_discipline = Locator(By.XPATH, '/html/body/div[4]/div[4]/div/div/div/div[1]/section[3]/div/div/div[2]/div[1]/ul/li[1]')
    discipline_save_button = Locator(By.CSS_SELECTOR, '#preprint-form-subjects .btn-primary')

    basics_tags_section = Locator(By.CSS_SELECTOR, '#preprint-form-basics .tagsinput')
    basics_tags_input = Locator(By.CSS_SELECTOR, '#preprint-form-basics .tagsinput input')
    basics_abstract_input = Locator(By.NAME, 'basicsAbstract')
    basics_save_button = Locator(By.CSS_SELECTOR, '#preprint-form-basics .btn-primary')

    create_preprint_button = Locator(By.CSS_SELECTOR, '.preprint-submit-body .submit-section > div > button.btn.btn-success.btn-md.m-t-md.pull-right')
    modal_create_preprint_button = Locator(By.CSS_SELECTOR, '.modal-footer button.btn-success:nth-child(2)', settings.LONG_TIMEOUT)


@pytest.mark.usefixtures('must_be_logged_in')
class PreprintDiscoverPage(BasePreprintPage):
    url_addition = 'discover'

    identity = Locator(By.ID, 'share-logo')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale')

    # Group Locators
    search_results = GroupLocator(By.CSS_SELECTOR, '.search-result h4 > a')


class PreprintDetailPage(GuidBasePage, BasePreprintPage):
    url_base = urljoin(settings.OSF_HOME, '{guid}')
    identity = Locator(By.ID, 'preprintTitle')
    title = Locator(By.ID, 'preprintTitle')
