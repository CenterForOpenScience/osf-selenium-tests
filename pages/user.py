import settings

from selenium.webdriver.common.by import By

from base.locators import Locator
from pages.base import GuidBasePage, OSFBasePage


class UserProfilePage(GuidBasePage):
    identity = Locator(By.CLASS_NAME, 'profile-fullname', settings.LONG_TIMEOUT)


class UserSettingsPage(OSFBasePage):
    url = settings.OSF_HOME + '/settings/'

    identity = Locator(By.ID, 'profileSettings')
