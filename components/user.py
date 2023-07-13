from selenium.webdriver.common.by import By

from base.locators import (
    BaseElement,
    Locator,
)


class SettingsSideNavigation(BaseElement):
    profile_information_link = Locator(By.LINK_TEXT, 'Profile information')
    account_settings_link = Locator(By.LINK_TEXT, 'Account settings')
    configure_addons_link = Locator(By.LINK_TEXT, 'Configure add-on accounts')
    notifications_link = Locator(By.LINK_TEXT, 'Notifications')
    developer_apps_link = Locator(By.LINK_TEXT, 'Developer apps')
    personal_access_tokens_link = Locator(By.LINK_TEXT, 'Personal access tokens')


class DeleteDevAppModal(BaseElement):
    app_name = Locator(By.CSS_SELECTOR, 'div.modal-header > h3 > strong')
    cancel_button = Locator(By.CSS_SELECTOR, 'button[data-test-cancel-delete]')
    delete_button = Locator(By.CSS_SELECTOR, 'button[data-test-confirm-delete]')


class DeletePATModal(BaseElement):
    token_name = Locator(By.CSS_SELECTOR, 'div.modal-header > h3 > strong')
    cancel_button = Locator(By.CSS_SELECTOR, 'button[data-test-cancel-delete]')
    delete_button = Locator(By.CSS_SELECTOR, 'button[data-test-confirm-delete]')


class ConfirmDeactivationRequestModal(BaseElement):
    cancel_button = Locator(By.CSS_SELECTOR, 'button[data-test-deactivation-cancel]')
    request_button = Locator(
        By.CSS_SELECTOR, 'button[data-test-confirm-deactivation-submit]'
    )


class UndoDeactivationRequestModal(BaseElement):
    cancel_button = Locator(By.CSS_SELECTOR, 'button[data-test-undo-warning-cancel]')
    undo_request_button = Locator(
        By.CSS_SELECTOR, 'button[data-test-undo-warning-confirm]'
    )


class Configure2FAModal(BaseElement):
    cancel_button = Locator(By.CSS_SELECTOR, '[data-test-enable-warning-cancel]')
    configure_button = Locator(By.CSS_SELECTOR, '[data-test-enable-warning-confirm]')


class ConfirmEmailSentModal(BaseElement):
    close_button = Locator(By.CSS_SELECTOR, '[data-test-close-modal]')


class ConfirmRemoveEmailModal(BaseElement):
    deleted_email = Locator(
        By.CSS_SELECTOR, '[data-test-delete-modal-body] > p > strong'
    )
    delete_button = Locator(By.CSS_SELECTOR, '[data-test-confirm-delete]')


class DeleteAffiliatedInstitutionModal(BaseElement):
    cancel_button = Locator(By.CSS_SELECTOR, 'button[data-test-cancel-delete]')
    delete_button = Locator(By.CSS_SELECTOR, 'button[data-test-confirm-delete]')
