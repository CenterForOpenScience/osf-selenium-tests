from selenium.webdriver.common.by import By

import settings
from api import osf_api
from base.locators import (
    ComponentLocator,
    GroupLocator,
    Locator,
)
from components.user import (
    Configure2FAModal,
    ConfirmDeactivationRequestModal,
    DeleteDevAppModal,
    DeletePATModal,
    SettingsSideNavigation,
    UndoDeactivationRequestModal,
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
    storage_location_listbox = Locator(
        By.CSS_SELECTOR, 'div[data-test-region-selector] > div'
    )
    configure_2fa_button = Locator(
        By.CSS_SELECTOR, 'button[data-test-two-factor-enable-button]'
    )
    two_facor_qr_code_img = Locator(By.CSS_SELECTOR, 'div[data-test-2f-qr-code] > img')
    cancel_2fa_button = Locator(
        By.CSS_SELECTOR, 'button[data-test-two-factor-verify-cancel-button]'
    )
    request_deactivation_button = Locator(
        By.CSS_SELECTOR, 'button[data-analytics-name="Deactivation request"]'
    )
    pending_deactivation_message = Locator(
        By.CSS_SELECTOR,
        'div[data-test-deactivation-panel] > div > div.panel-body > p:nth-child(3) > strong',
    )
    undo_deactivation_request_button = Locator(
        By.CSS_SELECTOR, 'button[data-analytics-name="Undo deactivation request"]'
    )
    configure_2fa_modal = ComponentLocator(Configure2FAModal)
    confirm_deactivation_modal = ComponentLocator(ConfirmDeactivationRequestModal)
    undo_deactivation_modal = ComponentLocator(UndoDeactivationRequestModal)


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


class PersonalAccessTokenPage(BaseUserSettingsPage):
    url = settings.OSF_HOME + '/settings/tokens/'

    identity = Locator(By.CSS_SELECTOR, 'h3[data-test-panel-title]')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-pulse')
    create_token_button = Locator(By.CSS_SELECTOR, '[data-test-create-token-link]')

    pat_cards = GroupLocator(By.CSS_SELECTOR, 'div[data-test-token-card]')

    delete_pat_modal = ComponentLocator(DeletePATModal)

    def get_pat_card_by_name(self, pat_name):
        for pat_card in self.pat_cards:
            token_name = pat_card.find_element_by_css_selector(
                '[data-analytics-name="Token name"]'
            )
            if pat_name in token_name.text:
                return pat_card


class CreatePersonalAccessTokenPage(BaseUserSettingsPage):
    url = settings.OSF_HOME + '/settings/tokens/create'

    identity = Locator(By.CSS_SELECTOR, '[data-test-token-name]')
    token_name_input = Locator(By.NAME, 'name')
    osf_users_profile_write_checkbox = Locator(
        By.CSS_SELECTOR, 'div[data-test-scope="osf.users.profile_write"] > input'
    )
    osf_full_write_checkbox = Locator(
        By.CSS_SELECTOR, 'div[data-test-scope="osf.full_write"] > input'
    )
    osf_nodes_full_write_checkbox = Locator(
        By.CSS_SELECTOR, 'div[data-test-scope="osf.nodes.full_write"] > input'
    )
    osf_nodes_full_read_checkbox = Locator(
        By.CSS_SELECTOR, 'div[data-test-scope="osf.nodes.full_read"] > input'
    )
    osf_nodes_metadata_write_checkbox = Locator(
        By.CSS_SELECTOR, 'div[data-test-scope="osf.nodes.metadata_write"] > input'
    )
    osf_full_read_checkbox = Locator(
        By.CSS_SELECTOR, 'div[data-test-scope="osf.full_read"] > input'
    )
    osf_nodes_metadata_read_checkbox = Locator(
        By.CSS_SELECTOR, 'div[data-test-scope="osf.nodes.metadata_read"] > input'
    )
    osf_nodes_access_read_checkbox = Locator(
        By.CSS_SELECTOR, 'div[data-test-scope="osf.nodes.access_read"] > input'
    )
    osf_nodes_access_write_checkbox = Locator(
        By.CSS_SELECTOR, 'div[data-test-scope="osf.nodes.access_write"] > input'
    )
    osf_nodes_data_read_checkbox = Locator(
        By.CSS_SELECTOR, 'div[data-test-scope="osf.nodes.data_read"] > input'
    )
    osf_nodes_data_write_checkbox = Locator(
        By.CSS_SELECTOR, 'div[data-test-scope="osf.nodes.data_write"] > input'
    )
    osf_users_email_read_checkbox = Locator(
        By.CSS_SELECTOR, 'div[data-test-scope="osf.users.email_read"] > input'
    )
    osf_users_profile_read_checkbox = Locator(
        By.CSS_SELECTOR, 'div[data-test-scope="osf.users.profile_read"] > input'
    )
    create_token_button = Locator(By.CSS_SELECTOR, '[data-test-create-token-button')


class EditPersonalAccessTokenPage(BaseUserSettingsPage):
    base_url = settings.OSF_HOME + '/settings/tokens/'

    identity = Locator(By.CSS_SELECTOR, 'div[data-analytics-scope="Edit"]')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-pulse')
    new_token_input = Locator(By.CSS_SELECTOR, 'div[data-test-new-token-value] > input')
    copy_to_clipboard_button = Locator(
        By.CSS_SELECTOR, 'div[data-test-new-token-value] > span > button'
    )
    back_to_list_of_tokens_link = Locator(
        By.CSS_SELECTOR, 'a[data-test-back-to-tokens]'
    )
    token_name_input = Locator(By.NAME, 'name')
    osf_users_profile_write_checkbox = Locator(
        By.CSS_SELECTOR, 'div[data-test-scope="osf.users.profile_write"] > input'
    )
    osf_full_write_checkbox = Locator(
        By.CSS_SELECTOR, 'div[data-test-scope="osf.full_write"] > input'
    )
    osf_nodes_full_write_checkbox = Locator(
        By.CSS_SELECTOR, 'div[data-test-scope="osf.nodes.full_write"] > input'
    )
    osf_nodes_full_read_checkbox = Locator(
        By.CSS_SELECTOR, 'div[data-test-scope="osf.nodes.full_read"] > input'
    )
    osf_nodes_metadata_write_checkbox = Locator(
        By.CSS_SELECTOR, 'div[data-test-scope="osf.nodes.metadata_write"] > input'
    )
    osf_full_read_checkbox = Locator(
        By.CSS_SELECTOR, 'div[data-test-scope="osf.full_read"] > input'
    )
    osf_nodes_metadata_read_checkbox = Locator(
        By.CSS_SELECTOR, 'div[data-test-scope="osf.nodes.metadata_read"] > input'
    )
    osf_nodes_access_read_checkbox = Locator(
        By.CSS_SELECTOR, 'div[data-test-scope="osf.nodes.access_read"] > input'
    )
    osf_nodes_access_write_checkbox = Locator(
        By.CSS_SELECTOR, 'div[data-test-scope="osf.nodes.access_write"] > input'
    )
    osf_nodes_data_read_checkbox = Locator(
        By.CSS_SELECTOR, 'div[data-test-scope="osf.nodes.data_read"] > input'
    )
    osf_nodes_data_write_checkbox = Locator(
        By.CSS_SELECTOR, 'div[data-test-scope="osf.nodes.data_write"] > input'
    )
    osf_users_email_read_checkbox = Locator(
        By.CSS_SELECTOR, 'div[data-test-scope="osf.users.email_read"] > input'
    )
    osf_users_profile_read_checkbox = Locator(
        By.CSS_SELECTOR, 'div[data-test-scope="osf.users.profile_read"] > input'
    )
    delete_button = Locator(By.CSS_SELECTOR, '[data-test-delete-button')
    save_button = Locator(By.CSS_SELECTOR, '[data-test-save-token-button')

    delete_pat_modal = ComponentLocator(DeletePATModal)

    def __init__(self, driver, verify=False, token_id=''):
        self.token_id = token_id
        super().__init__(driver, verify)

    @property
    def url(self):
        return self.base_url + self.token_id
