from selenium.webdriver.common.by import By
from base.locators import GroupLocator, BaseElement


class FileWidget(BaseElement):

    # Group Locators
    component_and_file_titles = GroupLocator(By.CSS_SELECTOR, '.td-title')
