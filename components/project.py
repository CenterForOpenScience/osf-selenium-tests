from selenium.webdriver.common.by import By
from base.locators import Locator, GroupLocator, BaseElement


class FileWidget(BaseElement):
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale')
    file_expander = Locator(By.CSS_SELECTOR, '.fa-plus')
    filter_button = Locator(By.CSS_SELECTOR, '.fangorn-toolbar-icon .fa-search')
    filter_input = Locator(By.CSS_SELECTOR, '#folderRow .form-control')

    # Group Locators
    component_and_file_titles = GroupLocator(By.CSS_SELECTOR, '.td-title')

class LogWidget(BaseElement):
    loading_indicator = Locator(By.CSS_SELECTOR, '#logFeed .ball-scale')

    # Group Locators
    log_items = GroupLocator(By.CSS_SELECTOR, '#logFeed .db-activity-item')
