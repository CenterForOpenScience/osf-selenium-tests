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
        names_list = []
        for schema in self.schema_list:
            names_list.append(schema.text)
        return names_list

    def select_schema_radio_button(self, schema_name='Open-Ended Registration'):
        """Selects the radio button corresponding to the given schema name"""
        for schema in self.schema_list:
            if schema.text == schema_name:
                schema.find_element_by_css_selector('.ember-view').click()


class ConfirmDeleteDraftRegistrationModal(BaseElement):
    cancel_button = Locator(By.CSS_SELECTOR, 'button[data-test-cancel-delete]')
    delete_button = Locator(By.CSS_SELECTOR, 'button[data-test-confirm-delete]')
