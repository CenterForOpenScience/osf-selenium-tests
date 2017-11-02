import settings

from pages.base import OSFBasePage
from selenium.webdriver.common.by import By


class LoginPage(OSFBasePage):

    locators = {
        **OSFBasePage.locators,
        **{
            'identity': (By.ID, 'fm1', settings.LONG_TIMEOUT),
            'username_input': (By.ID, 'username'),
            'password_input': (By.ID, 'password'),
            'submit_button': (By.NAME, 'submit'),
            'local_submit_button': (By.ID, 'submit'),
            'remember_me_checkbox': (By.ID, 'rememberMe'),
        }
    }
    
    def login(self, user, password):
        self.username_input.send_keys(user)
        if ('localhost:5000' in settings.OSF_HOME):
            self.local_submit_button.click()
        else:
            self.password_input.send_keys(password)
            if self.remember_me_checkbox.is_selected():
                self.remember_me_checkbox.click()
            self.submit_button.click()
