import settings

from pages.base import OSFBasePage, Locator
from selenium.webdriver.common.by import By


class LandingPage(OSFBasePage):
    url = settings.OSF_HOME

    # Locators
    identity = Locator(By.ID, 'home-hero', settings.LONG_TIMEOUT)
