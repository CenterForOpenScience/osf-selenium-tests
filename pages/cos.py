import settings

from time import sleep
from base.locators import Locator
from pages.base import BasePage
from selenium.webdriver.common.by import By


class COSDonatePage(BasePage):
    url = 'https://cos.io/about/support-cos/'

    identity = Locator(By.CSS_SELECTOR, 'div[class="slide-wrapper-background"', settings.LONG_TIMEOUT)
    page_heading = Locator(By.CSS_SELECTOR, 'div[class="banner-element"]')

    def verify(self):
        # TODO: Change this. This is bad
        if settings.BUILD == 'edge':
            sleep(.5)

        return self.page_heading.text == 'Public goods infrastructure should be free to use, but it\'s not free to build and maintain.'
