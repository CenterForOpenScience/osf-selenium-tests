import settings

from base.locators import Locator
from pages.base import BasePage
from selenium.webdriver.common.by import By


class COSDonatePage(BasePage):
    url = 'https://cos.io/about/support-cos/'

    identity = Locator(By.CSS_SELECTOR, 'div[class="slide-wrapper-background"]', settings.LONG_TIMEOUT)
    page_heading = Locator(By.CSS_SELECTOR, 'div[class="banner-element"]')
