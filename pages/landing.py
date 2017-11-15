import settings

from pages.base import OSFBasePage
from selenium.webdriver.common.by import By


class LandingPage(OSFBasePage):

    locators = {
        'identity': (By.ID, 'home-hero', settings.LONG_TIMEOUT),
    }
