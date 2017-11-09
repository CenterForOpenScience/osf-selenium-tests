import settings

from pages.base import OSFBasePage, BaseElement
from selenium.webdriver.common.by import By


class LandingPage(OSFBasePage):

    locators = {
        'identity': (By.CSS_SELECTOR, 'body > div.watermarked > div#home-hero > div.container.text-center > h1.hero-brand', settings.LONG_TIMEOUT),
    }

    def __init__(self, driver, verify=False):
        super(LandingPage, self).__init__(driver, verify, require_login=True)
