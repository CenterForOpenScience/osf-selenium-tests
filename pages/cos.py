import settings

from selenium.webdriver.common.by import By
from pages.base import BasePage, Locator


class COSDonatePage(BasePage):
    url = 'https://cos.io/about/donate-to-cos/'

    # Locators
    identity = Locator(By.CSS_SELECTOR, 'body > div.page-container > div.container.margin-bottom-30.margin-top-50 > div:nth-child(5) > div > div > div > h3 > b', settings.LONG_TIMEOUT)
