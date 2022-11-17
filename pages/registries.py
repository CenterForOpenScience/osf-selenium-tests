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

    narrative_summary = Locator(By.CSS_SELECTOR, '[data-test-read-only-response]')
    updates_dropdown = Locator(By.CSS_SELECTOR, '[data-test-update-button]')
    update_registration_button = Locator(
        By.CSS_SELECTOR, '[data-test-update-dropdown-create-new-revision]'
    )
    update_registration_dialogue = Locator(
        By.CSS_SELECTOR, '[data-test-new-update-dialog-main]'
    )
    update_registration_dialogue_next = Locator(
        By.CSS_SELECTOR, '[data-test-new-update-dialog-footer-next]'
    )


class RegistrationJustificationForm(GuidBasePage):
    identity = Locator(By.CSS_SELECTOR, '[data-test-link-back-to-registration]')

    justification_textbox = Locator(
        By.CSS_SELECTOR, 'textarea[name="revisionJustification"]'
    )
    justification_next_button = Locator(By.CSS_SELECTOR, '[data-test-goto-next-page]')
    cancel_update_button = Locator(By.CSS_SELECTOR, '[data-test-delete-button]')
    cancel_update_modal = Locator(
        By.CSS_SELECTOR, 'div[data-analytics-scope="Delete button modal"]'
    )
    confirm_cancel_button = Locator(By.CSS_SELECTOR, '[data-test-confirm-delete]')

    navbar_justification = Locator(By.CSS_SELECTOR, '[data-test-link="justification"]')
    navbar_summary = Locator(By.CSS_SELECTOR, '[data-test-link="1-summary"]')
    navbar_review = Locator(By.CSS_SELECTOR, '[data-test-link="review"]')

    summary_review_questions = Locator(
        By.CSS_SELECTOR, 'p[data-test-revised-responses-list-no-update]'
    )
    summary_textbox = Locator(By.CSS_SELECTOR, 'textarea[name="__responseKey_summary"]')
    summary_review_button = Locator(By.CSS_SELECTOR, '[data-test-goto-review]')

    submit_revision = Locator(By.CSS_SELECTOR, '[data-test-submit-revision]')
    accept_changes = Locator(By.CSS_SELECTOR, '[data-test-accept-changes]')
    toast_message = Locator(By.ID, 'toast-container')


class JustificationReviewForm(GuidBasePage):
    identity = Locator(By.ID, 'JustificationPageLabel')

    link_to_registration = Locator(
        By.CSS_SELECTOR, '[data-analytics-name="Go to registration"]'
    )


class RegistrationAddNewPage(BaseRegistriesPage):
    url_addition = 'new'
    identity = Locator(
        By.CSS_SELECTOR, 'form[data-test-new-registration-form]', settings.LONG_TIMEOUT
    )


class RegistrationDraftPage(BaseRegistriesPage):
    # This is a very generic draft registration page since it is using the side nav
    # bar as the locator which is on every draft page.
    identity = Locator(
        By.CSS_SELECTOR, 'nav[data-test-side-nav]', settings.LONG_TIMEOUT
    )


class DraftRegistrationMetadataPage(BaseRegistriesPage):
    identity = Locator(
        By.CSS_SELECTOR, 'div[data-test-metadata-title]', settings.LONG_TIMEOUT
    )


class DraftRegistrationReviewPage(BaseRegistriesPage):
    identity = Locator(
        By.CSS_SELECTOR,
        '[data-test-toggle-anchor-nav-button]',
        settings.LONG_TIMEOUT,
    )
