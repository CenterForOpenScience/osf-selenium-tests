import settings

from pages.base import BasePage
from selenium.webdriver.common.by import By
from pages.exceptions import HttpError, PageException


class LoginPage(BasePage):
    url = settings.OSF_HOME + '/login'

    locators = {
        'identity': (By.ID, 'login-page', settings.LONG_TIMEOUT),
        'username_input': (By.ID, 'username'),
        'password_input': (By.ID, 'password'),
        'submit_button': (By.NAME, 'submit'),
        'local_submit_button': (By.ID, 'submit'),
        'remember_me_checkbox': (By.ID, 'rememberMe'),
    }

    def __init__(self, driver):
        super(LoginPage, self).__init__(driver)
        driver.get(self.url)

        try:
            self.identity
        except ValueError:
            url = driver.current_url
            if url == (settings.OSF_HOME + '/'):
                raise HttpError(
                    driver=driver,
                    error_info='Already logged in'
                )
            raise PageException('Unexpected page structure: `{}`'.format(
                url
            ))


    def login(self, user, password):
        self.username_input.send_keys(user)
        if ('localhost:5000' in settings.OSF_HOME):
            self.local_submit_button.click()
        else:
            self.password_input.send_keys(password)
            if self.remember_me_checkbox.is_selected():
                self.remember_me_checkbox.click()
            self.submit_button.click()
