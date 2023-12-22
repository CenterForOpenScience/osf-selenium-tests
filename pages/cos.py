from selenium.webdriver.common.by import By

import settings
from base.locators import Locator
from pages.base import BasePage


class COSDonatePage(BasePage):
    url = 'https://www.cos.io/support-cos'

    identity = Locator(By.ID, 'Yourdonationtitle', settings.LONG_TIMEOUT)
