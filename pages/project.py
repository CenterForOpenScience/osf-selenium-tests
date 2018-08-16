import settings

from selenium.webdriver.common.by import By

from components.project import FileWidget, LogWidget
from pages.base import GuidBasePage, OSFBasePage
from base.locators import Locator, ComponentLocator


class ProjectPage(GuidBasePage):
    identity = Locator(By.CSS_SELECTOR, '#overview > nav#projectSubnav')
    title = Locator(By.ID, 'nodeTitleEditable', settings.LONG_TIMEOUT)
    title_input = Locator(By.CSS_SELECTOR, '.form-inline input')
    title_edit_submit_button = Locator(By.CSS_SELECTOR, '.editable-submit')
    title_edit_cancel_button = Locator(By.CSS_SELECTOR, '.editable-cancel')
    make_public_link = Locator(By.XPATH, '//a[contains(text(), "Make Public")]')
    make_private_link = Locator(By.XPATH, '//a[contains(text(), "Make Private")]')
    confirm_privacy_change_link = Locator(By.XPATH, '//a[text()="Confirm"]')
    cancel_privacy_change_link = Locator(By.XPATH, '//a[text()="Cancel"]')

    # Components
    file_widget = ComponentLocator(FileWidget)
    log_widget = ComponentLocator(LogWidget)


class MyProjectsPage(OSFBasePage):
    url = settings.OSF_HOME + '/myprojects/'

    identity = Locator(By.CSS_SELECTOR, '.col-xs-8 > h3:nth-child(1)')
