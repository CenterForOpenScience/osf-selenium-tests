from selenium.webdriver.common.by import By

import settings
from base.exceptions import LoginError
from base.locators import Locator, GroupLocator
from pages.base import BasePage, OSFBasePage


class LoginPage(BasePage):
    url = settings.OSF_HOME + '/login'

    identity = Locator(By.ID, 'loginForm', settings.LONG_TIMEOUT)
    username_input = Locator(By.ID, 'username')
    password_input = Locator(By.ID, 'password')
    submit_button = Locator(By.NAME, 'submit')
    remember_me_checkbox = Locator(By.ID, 'rememberMe')
    institutional_login_button = Locator(By.ID, 'instnLogin')
    orcid_login_button = Locator(By.ID, 'orcidlogin')
    osf_home_link = Locator(By.CSS_SELECTOR, '.navbar-link')
    sign_up_button = Locator(By.ID, 'osfRegister')
    reset_password_link = Locator(By.CSS_SELECTOR, 'span.cas-field-float-right > a:nth-child(1)')
    need_help_link = Locator(By.CSS_SELECTOR, 'span.cas-field-float-right > a:nth-child(3)')
    cos_footer_link = Locator(By.CSS_SELECTOR, '#copyright > a:nth-child(2)')
    terms_of_use_footer_link = Locator(By.CSS_SELECTOR, '#copyright > a:nth-child(3)')
    privacy_policy_footer_link = Locator(By.CSS_SELECTOR, '#copyright > a:nth-child(4)')
    status_footer_link = Locator(By.CSS_SELECTOR, '#copyright > a:nth-child(5)')

    if 'localhost:5000' in settings.OSF_HOME:
        submit_button = Locator(By.ID, 'submit')
        identity = Locator(By.ID, 'login')

    def error_handling(self):
        if '/login' not in self.driver.current_url:
            raise LoginError('Already logged in')

    def submit_login(self, user, password):
        self.username_input.send_keys(user)
        if ('localhost:5000' not in settings.OSF_HOME):
            self.password_input.send_keys(password)
            if self.remember_me_checkbox.is_selected():
                self.remember_me_checkbox.click()
        self.submit_button.click()


class InstitutionalLoginPage(BasePage):
    url = settings.OSF_HOME + '/login?campaign=institution'

    identity = Locator(By.CSS_SELECTOR, '#institutionSelect')
    institution_dropdown = Locator(By.ID, 'institutionSelect')
    sign_in_button = Locator(By.ID, 'institutionSubmit')
    osf_home_link = Locator(By.CSS_SELECTOR, '.navbar-link')
    sign_up_button = Locator(By.ID, 'osfRegister')
    cant_find_institution_link = Locator(By.CSS_SELECTOR, '#content > div > section > section:nth-child(5) > span > a')
    need_help_link = Locator(By.CSS_SELECTOR, '#content > div > section > section:nth-child(8) > span > a')
    sign_in_with_osf_link = Locator(By.CSS_SELECTOR, '#content > div > section > section:nth-child(9) > span > a')
    cos_footer_link = Locator(By.CSS_SELECTOR, '#copyright > a:nth-child(2)')
    terms_of_use_footer_link = Locator(By.CSS_SELECTOR, '#copyright > a:nth-child(3)')
    privacy_policy_footer_link = Locator(By.CSS_SELECTOR, '#copyright > a:nth-child(4)')
    status_footer_link = Locator(By.CSS_SELECTOR, '#copyright > a:nth-child(5)')

    dropdown_options = GroupLocator(By.CSS_SELECTOR, '#institutionSelect option')


class ForgotPasswordPage(BasePage):
    url = settings.OSF_HOME + '/forgotpassword/'

    identity = Locator(By.ID, 'forgotPasswordForm')


class UnsupportedInstitutionLoginPage(BasePage):
    url = settings.OSF_HOME + '/login?campaign=unsupportedinstitution'

    identity = Locator(By.ID, 'osfUnsupportedInstitutionLogin')


def login(driver, user=settings.USER_ONE, password=settings.USER_ONE_PASSWORD):
    login_page = LoginPage(driver)
    login_page.goto()
    login_page.submit_login(user, password)


def safe_login(driver, user=settings.USER_ONE, password=settings.USER_ONE_PASSWORD):
    """Raise a LoginError if login fails.
    """
    login(driver, user=user, password=password)
    if not OSFBasePage(driver).is_logged_in():
        raise LoginError('Login failed')


def logout(driver):
    """Log the user out.
    """
    driver.get(settings.OSF_HOME + '/logout/')
