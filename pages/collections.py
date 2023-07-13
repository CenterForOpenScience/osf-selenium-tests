from urllib.parse import urljoin

from selenium.webdriver.common.by import By

import settings
from base.locators import (
    ComponentLocator,
    GroupLocator,
    Locator,
)
from components.navbars import CollectionsNavbar
from pages.base import OSFBasePage


class BaseCollectionPage(OSFBasePage):
    """The base page from which all collection pages inherit."""

    base_url = settings.OSF_HOME + '/collections/'
    url_addition = ''
    navbar = ComponentLocator(CollectionsNavbar)

    def __init__(self, driver, verify=False, provider=None):
        self.provider = provider
        if provider:
            self.provider_id = provider['id']
            self.provider_name = provider['attributes']['name']

        super().__init__(driver, verify)

    @property
    def url(self):
        """Set the URL based on the provider domain."""
        return urljoin(self.base_url, self.provider_id) + '/' + self.url_addition

    def verify(self):
        """Return true if you are on the expected page.
        Checks both the general page identity and the branding.
        """
        if self.provider:
            return super().verify() and self.provider_name in self.navbar.title.text
        return super().verify()


class CollectionDiscoverPage(BaseCollectionPage):
    url_addition = 'discover'

    identity = Locator(By.CSS_SELECTOR, 'div[data-test-provider-branding]')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale')


class CollectionSubmitPage(BaseCollectionPage):
    url_addition = 'submit'

    identity = Locator(By.CSS_SELECTOR, 'div[data-test-collections-submit-sections]')
    project_selector = Locator(
        By.CSS_SELECTOR, 'span[class="ember-power-select-placeholder"]'
    )
    project_help_text = Locator(
        By.CSS_SELECTOR, '.ember-power-select-option--search-message'
    )
    project_selector_project = Locator(By.CSS_SELECTOR, '.ember-power-select-option')
    license_dropdown_trigger = Locator(
        By.CSS_SELECTOR, '[data-test-power-select-dropdown]'
    )
    first_license_option = Locator(
        By.CSS_SELECTOR, '.ember-power-select-options > li:nth-child(1)'
    )
    description_textbox = Locator(By.CSS_SELECTOR, 'textarea[name="description"]')
    tags_input = Locator(By.CLASS_NAME, 'emberTagInput-input')
    project_metadata_save = Locator(
        By.CSS_SELECTOR, '[data-test-project-metadata-save-button]'
    )
    project_contributors_continue = Locator(
        By.CSS_SELECTOR, '[data-test-submit-section-continue]'
    )
    type_dropdown_trigger = Locator(
        By.CLASS_NAME,
        'ember-view.ember-basic-dropdown-trigger.ember-power-select-trigger',
    )
    first_type_option = Locator(
        By.CSS_SELECTOR, '.ember-power-select-options > li:nth-child(1)'
    )
    collection_metadata_continue = Locator(
        By.CSS_SELECTOR, '[data-test-submit-section-continue]'
    )
    add_to_collection_button = Locator(
        By.CSS_SELECTOR, '[data-test-collections-submit-submit-button]'
    )
    modal_add_to_collection_button = Locator(
        By.CSS_SELECTOR,
        '[data-test-collection-submission-confirmation-modal-add-button]',
    )


class CollectionEditPage(BaseCollectionPage):
    url_addition = '{guid}/edit'

    identity = Locator(By.CSS_SELECTOR, 'div[data-test-submit-section-click-to-edit]')
    remove_button = Locator(
        By.CSS_SELECTOR, 'span[data-test-collections-remove-button] > button'
    )
    modal_remove_reason_input = Locator(
        By.CSS_SELECTOR, 'textarea[data-test-collections-remove-reason]'
    )
    modal_cancel_remove_button = Locator(
        By.CSS_SELECTOR, 'button[data-test-cancel-delete]'
    )
    modal_remove_button = Locator(By.CSS_SELECTOR, 'button[data-test-confirm-delete]')

    def __init__(self, driver, verify=False, provider=None, guid=''):
        self.guid = guid
        super().__init__(driver, verify, provider)

    @property
    def url(self):
        return (
            urljoin(self.base_url, self.provider_id)
            + '/'
            + self.url_addition.format(guid=self.guid)
        )


class BaseCollectionModerationPage(BaseCollectionPage):
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale')

    submission_cards = GroupLocator(By.CSS_SELECTOR, '[data-test-submission-card]')

    def get_submission_card(self, node_id):
        for card in self.submission_cards:
            url = card.find_element_by_css_selector(
                '[data-test-submission-card-title]'
            ).get_attribute('href')
            guid = url.split(settings.OSF_HOME + '/', 1)[1]
            if guid == node_id:
                return card
        return None


class CollectionModerationPendingPage(BaseCollectionModerationPage):
    url_addition = 'moderation/all?state=pending#'
    identity = Locator(
        By.CSS_SELECTOR, '[data-test-submissions-type="pending"]', settings.LONG_TIMEOUT
    )
    accept_radio_button = Locator(By.CSS_SELECTOR, 'input[value="accept"]')
    reject_radio_button = Locator(By.CSS_SELECTOR, 'input[value="reject"]')
    moderation_comment = Locator(
        By.CSS_SELECTOR, '[data-test-moderation-dropdown-comment]'
    )
    submit_button = Locator(
        By.CSS_SELECTOR, 'button[data-test-moderation-dropdown-submit]'
    )


class CollectionModerationAcceptedPage(BaseCollectionModerationPage):
    url_addition = 'moderation/all?state=accepted#'
    identity = Locator(
        By.CSS_SELECTOR,
        '[data-test-submissions-type="accepted"]',
        settings.LONG_TIMEOUT,
    )
    remove_radio_button = Locator(By.CSS_SELECTOR, 'input[value="remove"]')
    moderation_comment = Locator(
        By.CSS_SELECTOR, '[data-test-moderation-dropdown-comment]'
    )
    submit_button = Locator(
        By.CSS_SELECTOR, 'button[data-test-moderation-dropdown-submit]'
    )


class CollectionModerationRejectedPage(BaseCollectionModerationPage):
    url_addition = 'moderation/all?state=rejected'
    identity = Locator(
        By.CSS_SELECTOR,
        '[data-test-submissions-type="rejected"]',
        settings.LONG_TIMEOUT,
    )


class CollectionModerationRemovedPage(BaseCollectionModerationPage):
    url_addition = 'moderation/all?state=removed'
    identity = Locator(
        By.CSS_SELECTOR,
        '[data-test-submissions-type="removed"]',
        settings.LONG_TIMEOUT,
    )
