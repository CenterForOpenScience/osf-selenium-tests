from selenium.webdriver.common.by import By
from pages.base import BasePage, Locator


class COSDonatePage(BasePage):
    url = 'https://cos.io/about/donate-to-cos/'

    # Locators
    page_heading = Locator(By.CSS_SELECTOR, 'body > div.page-container > div.container.margin-bottom-30.margin-top-50 > h1 > strong')

    def verify(self):
        return self.page_heading.text == 'Public goods infrastructure should be free to use, but it\'s not free to build and maintain.'
