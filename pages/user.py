import settings

from api import osf_api
from selenium.webdriver.common.by import By

from base.locators import Locator, GroupLocator
from pages.base import GuidBasePage, OSFBasePage


class UserProfilePage(GuidBasePage):
    user = osf_api.current_user()

    def __init__(self, driver, verify=False, guid=user.id):
        super().__init__(driver, verify, guid)

    #TODO: Reconsider using a component here (and using component locators correctly)
    identity = Locator(By.CLASS_NAME, 'profile-fullname', settings.LONG_TIMEOUT)
    no_public_projects_text = Locator(By.CSS_SELECTOR, '#publicProjects .help-block')
    no_public_components_text = Locator(By.CSS_SELECTOR, '#publicComponents .help-block')
    edit_profile_link = Locator(By.CSS_SELECTOR, '#edit-profile-settings')

    #TODO: Seperate out by component if it becomes necessary
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-pulse')

    # Group locators
    public_projects = GroupLocator(By.CSS_SELECTOR, '#publicProjects .list-group-item')
    public_components = GroupLocator(By.CSS_SELECTOR, '#publicComponents .list-group-item')
    quickfiles = GroupLocator(By.CSS_SELECTOR, '#quickFiles .list-group-item')


class UserSettingsPage(OSFBasePage):
    url = settings.OSF_HOME + '/settings/'

    identity = Locator(By.ID, 'profileSettings')
