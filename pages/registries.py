from urllib.parse import urljoin

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
    base_url = urljoin(settings.OSF_HOME, 'registries/')
    url_addition = ''
    navbar = ComponentLocator(RegistriesNavbar)

    def __init__(self, driver, verify=False, provider=None):
        self.provider = provider
        if provider:
            self.provider_id = provider['id']
            self.provider_name = provider['attributes']['name']

        super().__init__(driver, verify)

    @property
    def url(self):
        """Set the URL based on the provider except when the provider is OSF."""
        if self.provider and self.provider_id != 'osf':
            self.base_url = urljoin(self.base_url, self.provider_id) + '/'
        return urljoin(self.base_url, self.url_addition)


class RegistriesLandingPage(BaseRegistriesPage):
    identity = Locator(
        By.CSS_SELECTOR, '._RegistriesHeader_3zbd8x', settings.LONG_TIMEOUT
    )
    search_box = Locator(By.ID, 'search')


class RegistriesDiscoverPage(BaseRegistriesPage):
    url_addition = 'discover'

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
    url_addition = 'new'
    identity = Locator(
        By.CSS_SELECTOR, 'form[data-test-new-registration-form]', settings.LONG_TIMEOUT
    )


class RegistrationDraftPage(BaseRegistriesPage):
    identity = Locator(
        By.CSS_SELECTOR, 'nav[data-test-side-nav]', settings.LONG_TIMEOUT
    )
