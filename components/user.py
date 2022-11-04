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
