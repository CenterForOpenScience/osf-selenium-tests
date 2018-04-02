import settings

from selenium.webdriver.common.by import By

from base.locators import Locator
from pages.base import OSFBasePage

class SearchPage(OSFBasePage):
    url = settings.OSF_HOME + '/search/'

    identity = Locator(By.ID, 'searchPageFullBar')
