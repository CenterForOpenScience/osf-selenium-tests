from selenium.webdriver.common.by import By

import settings
from api import osf_api
from base.locators import (
    ComponentLocator,
    GroupLocator,
    Locator,
)
from components.user import (
    DeleteDevAppModal,
    SettingsSideNavigation,
)
from pages.base import (
    GuidBasePage,
    OSFBasePage,
)


class UserProfilePage(GuidBasePage):
    user = osf_api.current_user()

    def __init__(self, driver, verify=False, guid=user.id):
        super().__init__(driver, verify, guid)

    # TODO: Reconsider using a component here (and using component locators correctly)
    identity = Locator(By.CLASS_NAME, 'profile-fullname', settings.LONG_TIMEOUT)
    no_public_projects_text = Locator(By.CSS_SELECTOR, '#publicProjects .help-block')
    no_public_components_text = Locator(
        By.CSS_SELECTOR, '#publicComponents .help-block'
    )
    edit_profile_link = Locator(By.CSS_SELECTOR, '#edit-profile-settings')

    # TODO: Seperate out by component if it becomes necessary
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-pulse', settings.LONG_TIMEOUT)

    # Group Locators
    public_projects = GroupLocator(By.CSS_SELECTOR, '#publicProjects .list-group-item')
    public_components = GroupLocator(
        By.CSS_SELECTOR, '#publicComponents .list-group-item'
    )


class BaseUserSettingsPage(OSFBasePage):
    url = settings.OSF_HOME + '/settings/'

    identity = Locator(By.ID, 'profileSettings')

    # Components
    side_navigation = ComponentLocator(SettingsSideNavigation)


class ProfileInformationPage(BaseUserSettingsPage):
    url = settings.OSF_HOME + '/settings/'

    identity = Locator(By.CSS_SELECTOR, 'div[id="profileSettings"]')
    middle_name_input = Locator(
        By.CSS_SELECTOR, '#names > div > form > div:nth-child(5) > input'
    )
    save_button = Locator(
        By.CSS_SELECTOR,
        '#names > div > form > div.p-t-lg.p-b-lg > button.btn.btn-success',
    )
    update_success = Locator(By.CSS_SELECTOR, '.text-success')


class AccountSettingsPage(BaseUserSettingsPage):
    url = settings.OSF_HOME + '/settings/account/'

    identity = Locator(
        By.CSS_SELECTOR, 'div[data-analytics-scope="Connected emails panel"]'
    )


class ConfigureAddonsPage(BaseUserSettingsPage):
    url = settings.OSF_HOME + '/settings/addons/'

    identity = Locator(By.CSS_SELECTOR, '#configureAddons')


class NotificationsPage(BaseUserSettingsPage):
    url = settings.OSF_HOME + '/settings/notifications/'

    identity = Locator(By.CSS_SELECTOR, '#notificationSettings')


class DeveloperAppsPage(BaseUserSettingsPage):
    url = settings.OSF_HOME + '/settings/applications/'

    identity = Locator(By.CSS_SELECTOR, 'div[data-analytics-scope="Developer apps"')
    create_dev_app_button = Locator(By.CSS_SELECTOR, '[data-test-create-app-link]')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-pulse', settings.LONG_TIMEOUT)

    dev_app_cards = GroupLocator(By.CSS_SELECTOR, 'div[data-test-developer-app-card]')

    delete_dev_app_modal = ComponentLocator(DeleteDevAppModal)

    def get_dev_app_card_by_app_name(self, app_name):
        for dev_app_card in self.dev_app_cards:
            dev_app_name = dev_app_card.find_element_by_css_selector(
                '[data-analytics-name="App name"]'
            )
            if app_name in dev_app_name.text:
                return dev_app_card


class CreateDeveloperAppPage(BaseUserSettingsPage):
    url = settings.OSF_HOME + '/settings/applications/create'

    identity = Locator(By.CSS_SELECTOR, '[data-test-developer-app-name]')
    app_name_input = Locator(By.NAME, 'name')
    project_url_input = Locator(By.NAME, 'homeUrl')
    app_description_textarea = Locator(
        By.CSS_SELECTOR, 'div[data-test-developer-app-description] > div > textarea'
    )
    callback_url_input = Locator(By.NAME, 'callbackUrl')
    create_dev_app_button = Locator(
        By.CSS_SELECTOR, '[data-test-create-developer-app-button]'
    )


class EditDeveloperAppPage(BaseUserSettingsPage):
    base_url = settings.OSF_HOME + '/settings/applications/'

    identity = Locator(By.CSS_SELECTOR, '[data-test-client-id]')
    client_id_input = Locator(By.CSS_SELECTOR, 'div[data-test-client-id] > input')
    client_secret_input = Locator(
        By.CSS_SELECTOR, 'div[data-test-client-secret] > input'
    )
    show_client_secret_button = Locator(
        By.CSS_SELECTOR, '[data-test-toggle-client-secret]'
    )
    app_name_input = Locator(By.NAME, 'name')
    project_url_input = Locator(By.NAME, 'homeUrl')
    app_description_textarea = Locator(
        By.CSS_SELECTOR, 'div[data-test-developer-app-description] > div > textarea'
    )
    callback_url_input = Locator(By.NAME, 'callbackUrl')
    save_button = Locator(By.CSS_SELECTOR, '[data-test-save-developer-app-button]')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-pulse', settings.LONG_TIMEOUT)

    def __init__(self, driver, verify=False, client_id=''):
        self.client_id = client_id
        super().__init__(driver, verify)

    @property
    def url(self):
        return self.base_url + self.client_id


class EmberPersonalAccessTokenPage(BaseUserSettingsPage):
    url = settings.OSF_HOME + '/settings/tokens/'

    identity = Locator(By.CSS_SELECTOR, '[data-test-create-token-link]')


class PersonalAccessTokenPage(BaseUserSettingsPage):
    waffle_override = {'ember_user_settings_tokens_page': EmberPersonalAccessTokenPage}

    url = settings.OSF_HOME + '/settings/tokens/'

    identity = Locator(By.CSS_SELECTOR, 'a[data-analytics-name="Personal access"]')
