import settings

from pages.base import OSFBasePage
from selenium.webdriver.common.by import By


class LandingPage(OSFBasePage):
    url = settings.OSF_HOME

    locators = {
        'identity': (By.ID, 'home-hero', settings.LONG_TIMEOUT),
    }
