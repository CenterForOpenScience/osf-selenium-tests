import settings

from base.locators import Locator
from selenium.webdriver.common.by import By
from pages.base import OSFBasePage


class EmberRegisterPage(OSFBasePage):
    url = settings.OSF_HOME + '/register'

    identity = Locator(By.CSS_SELECTOR, '._sign-up-container_19kgff')


class RegisterPage(OSFBasePage):

    waffle_override = {'ember_auth_register': EmberRegisterPage}

    url = settings.OSF_HOME + '/register'

    identity = Locator(By.CSS_SELECTOR, '#signUpScope')
