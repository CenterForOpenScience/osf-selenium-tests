import settings

from selenium.webdriver.common.by import By

from base.locators import Locator
from pages.base import OSFBasePage


class EmberSupportPage(OSFBasePage):
    url = settings.OSF_HOME + '/support'

    identity = Locator(By.CSS_SELECTOR, '._Support_15i3vw', settings.LONG_TIMEOUT)


class SupportPage(OSFBasePage):
    waffle_override = {'ember_support_page': EmberSupportPage}

    identity = Locator(By.CSS_SELECTOR, 'body > div.watermarked > div > div > h1', settings.LONG_TIMEOUT)
