import settings

from base.locators import Locator
from selenium.webdriver.common.by import By
from pages.base import OSFBasePage


class RegisterPage(OSFBasePage):
    url = settings.OSF_HOME + '/register'

    identity = Locator(By.CSS_SELECTOR, '#signUpScope')
