from selenium.webdriver.common.by import By

import settings
from base.locators import (
    BaseElement,
    GroupLocator,
    Locator,
)


class FileWidget(BaseElement):
    loading_indicator = Locator(
        By.CSS_SELECTOR, '#treeGrid .ball-scale', settings.VERY_LONG_TIMEOUT
    )
    file_expander = Locator(By.CSS_SELECTOR, '.fa-plus')
    filter_button = Locator(By.CSS_SELECTOR, '.fangorn-toolbar-icon .fa-search')
    filter_input = Locator(By.CSS_SELECTOR, '#folderRow .form-control')
    first_file = Locator(By.CSS_SELECTOR, 'div[data-level="3"] > .td-title')

    # Group Locators
    component_and_file_titles = GroupLocator(By.CSS_SELECTOR, '.td-title')


class LogWidget(BaseElement):
    loading_indicator = Locator(By.CSS_SELECTOR, '#logFeed .ball-scale')

    # Group Locators
    log_items = GroupLocator(By.CSS_SELECTOR, '#logFeed .db-activity-item')


class CreateRegistrationModal(BaseElement):
    modal_window = Locator(By.CSS_SELECTOR, '[data-test-new-registration-modal]')
    cancel_button = Locator(
        By.CSS_SELECTOR, 'button[data-test-new-registration-modal-cancel-button]'
    )
    create_draft_button = Locator(
        By.CSS_SELECTOR, 'button[data-test-new-registration-modal-create-draft-button]'
    )

    # Group Locators
    schema_list = GroupLocator(
        By.CSS_SELECTOR, '[data-test-new-registration-modal-schema]'
    )

    def get_schema_names_list(self):
        """Returns the schema names from the schema list"""
        return [schema.text for schema in self.schema_list]

    def select_schema_radio_button(self, schema_name='Open-Ended Registration'):
        """Selects the radio button corresponding to the given schema name"""
        for schema in self.schema_list:
            if schema.text == schema_name:
                schema.find_element_by_css_selector('.ember-view').click()
                break


class ConfirmDeleteDraftRegistrationModal(BaseElement):
    cancel_button = Locator(By.CSS_SELECTOR, 'button[data-test-cancel-delete]')
    delete_button = Locator(By.CSS_SELECTOR, 'button[data-test-confirm-delete]')


class ConfirmFileDeleteModal(BaseElement):
    """There are actually multiple almost identical versions of the Confirm Delete Modal
    on the Project Files page. So we use the GroupLocator to locate the Cancel and Delete
    buttons which are identical, and then use indexing of these elements when interacting
    with them in the tests.
    """

    heading = Locator(By.ID, 'osf-dialog-heading')
    cancel_button = GroupLocator(
        By.CSS_SELECTOR,
        'button._Button_6kisxq._MediumButton_6kisxq._SecondaryButton_6kisxq',
    )
    delete_button = GroupLocator(
        By.CSS_SELECTOR,
        'button._Button_6kisxq._MediumButton_6kisxq._DestroyButton_6kisxq',
    )
    done_button = Locator(By.CSS_SELECTOR, 'div._Footer_gyio2l > button')


class MoveCopyFileModal(BaseElement):
    project_link = Locator(
        By.CSS_SELECTOR, '[data-test-go-to-current-node-file-providers]'
    )
    provider_osfstorage_link = Locator(
        By.CSS_SELECTOR, '[data-test-move-to-folder="osfstorage"]'
    )
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-pulse')
    cancel_button = Locator(
        By.CSS_SELECTOR,
        'div._Footer_gyio2l > button._Button_6kisxq._MediumButton_6kisxq._SecondaryButton_6kisxq',
    )
    move_copy_button = Locator(By.CSS_SELECTOR, '[data-test-move-files-button]')
    in_process_ind = Locator(By.CSS_SELECTOR, '[data-icon="spinner"]')
    done_button = Locator(By.CSS_SELECTOR, '[data-test-move-done-button]')


class RenameFileModal(BaseElement):
    rename_input_box = Locator(By.CSS_SELECTOR, '[data-test-user-input]')
    save_button = Locator(By.CSS_SELECTOR, '[data-test-disabled-rename]')
