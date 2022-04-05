from selenium.webdriver.common.by import By

import settings
from base.locators import Locator
from pages.base import OSFBasePage


class SupportPage(OSFBasePage):
    url = 'https://help.osf.io/'

    identity = Locator(By.CSS_SELECTOR, 'img[alt="OSF Support"]', settings.LONG_TIMEOUT)
