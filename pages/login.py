import settings

from pages.exceptions import LoginError
from selenium.webdriver.common.by import By
from pages.base import BasePage, Locator, OSFBasePage


class LoginPage(BasePage):
    url = settings.OSF_HOME + '/login'

    # Locators
    identity = Locator(By.XPATH, '/html/body[@id="cas"]/div[@id="container"]', settings.LONG_TIMEOUT)
    username_input = Locator(By.ID, 'username')
    password_input = Locator(By.ID, 'password')
    submit_button = Locator(By.NAME, 'submit')
    remember_me_checkbox = Locator(By.ID, 'rememberMe')

    if 'localhost:5000' in settings.OSF_HOME:
        submit_button = Locator(By.ID, 'submit')
        identity = Locator(By.ID, 'login')

    def error_handling(self):
        if '/login' not in self.driver.current_url:
            raise LoginError(
                driver=self.driver,
                error_info='Already logged in'
            )

    def submit_login(self, user, password):
        self.username_input.send_keys(user)
        if ('localhost:5000' not in settings.OSF_HOME):
            self.password_input.send_keys(password)
            if self.remember_me_checkbox.is_selected():
                self.remember_me_checkbox.click()
        self.submit_button.click()

def login(driver, user=settings.USER_ONE, password=settings.USER_ONE_PASSWORD):
    login_page = LoginPage(driver)
    login_page.goto()
    login_page.submit_login(user, password)

def safe_login(driver):
    driver.get(settings.OSF_HOME)
    if OSFBasePage(driver).is_logged_out():
        login(driver)

def logout(driver):
    driver.get(settings.OSF_HOME + '/logout/')
