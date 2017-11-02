import settings

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

from pages.exceptions import HttpError, PageException


class BaseElement(object):
    default_timeout = settings.TIMEOUT

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, *loc):
        return self.driver.find_element(*loc)

    def verify(self):
        raise NotImplementedError

    def __getattr__(self, element):
        """
        This method is adapted from code provided on seleniumframework.com
        """
        timeout = self.default_timeout

        if element in self.locators:
            if len(self.locators[element]) == 3:
                timeout = self.locators[element][2]
            location = (self.locators[element][0], self.locators[element][1])

            try:
                WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(location)
                )
            except(TimeoutException, StaleElementReferenceException):
                raise ValueError('Element {} not present on page'.format(element))

            try:
                WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located(location)
                )
            except(TimeoutException, StaleElementReferenceException):
                raise ValueError('Element {} not visible before timeout'.format(element))

            if 'link' in element:
                try:
                    WebDriverWait(self.driver, timeout).until(
                        EC.element_to_be_clickable(location)
                    )
                except(TimeoutException, StaleElementReferenceException):
                    raise ValueError('Element {} on page but not clickable'.format(element))

            return self.find_element(*location)
        else:
            raise ValueError('Cannot find element {}'.format(element))


class BasePage(BaseElement):
    url = None

    def goto(self):
        self.driver.get(self.url)

    def reload(self):
        self.driver.refresh()


class Navbar(BaseElement):

    locators = {
        'service_dropdown': (By.CSS_SELECTOR, '#navbarScope > div.container > div.navbar-header > div.dropdown > button'),
        'home_link': (By.CSS_SELECTOR, '#navbarScope > div.container > div.navbar-header > div.dropdown > ul > li:nth-child(1) > a'),
        'preprints_link': (By.CSS_SELECTOR, '#navbarScope > div.container > div.navbar-header > div.dropdown > ul > li:nth-child(2) > a'),
        'registries_link': (By.CSS_SELECTOR, '#navbarScope > div.container > div.navbar-header > div.dropdown > ul > li:nth-child(3) > a'),
        'meetings_link': (By.CSS_SELECTOR, '#navbarScope > div.container > div.navbar-header > div.dropdown > ul > li:nth-child(4) > a'),
        'search_link': (By.CSS_SELECTOR, '#secondary-navigation > ul > li:nth-last-child(4) > a'),
        'support_link': (By.CSS_SELECTOR, '#secondary-navigation > ul > li:nth-last-child(3) > a'),
        'donate_link': (By.CSS_SELECTOR, '#secondary-navigation > ul > li:nth-last-child(2) > a'),
        'user_dropdown': (By.CSS_SELECTOR, '#secondary-navigation > ul > li:nth-last-child(1) > button'),
        'user_dropdown_profile': (By.CSS_SELECTOR, '#secondary-navigation > ul > li.dropdown.open > ul > li:nth-child(1) > a'),
        'user_dropdown_support': (By.CSS_SELECTOR, '#secondary-navigation > ul > li.dropdown.open > ul > li:nth-child(2) > a'),
        'user_dropdown_settings': (By.CSS_SELECTOR, '#secondary-navigation > ul > li.dropdown.open > ul > li:nth-child(3) > a'),
        'sign_up_button': (By.LINK_TEXT, 'Sign Up'),
        'sign_in_button': (By.LINK_TEXT, 'Sign In'),
        'logout_link': (By.CSS_SELECTOR, '#secondary-navigation > ul > li.dropdown.open > ul > li:nth-child(4) > a'),
        'current_service': (By.CSS_SELECTOR, '#navbarScope > div > div > div.service-home > a > span.current-service > strong')
    }

    def verify(self):
        return len(self.find_elements(By.ID, 'navbarScope')) == 1

    def is_logged_in(self):
        try:
            if self.sign_in_button:
                return False
        except ValueError:
            return True


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
        old_url = driver.current_url
        driver.get(self.url)

        try:
            self.identity
        except ValueError:
            url = driver.current_url
            if url == old_url:
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


def login(osf_page, user=settings.USER_ONE, password=settings.USER_ONE_PASSWORD):
    try:
        login_page = LoginPage(osf_page.driver)
    except HttpError:
        pass
    else:
        login_page.login(user, password)
        osf_page.driver.get(osf_page.url)


class OSFBasePage(BasePage):
    url = settings.OSF_HOME

    # all page must have unique identity
    locators = {
        'identity': (By.LINK_TEXT, 'Center for Open Science'),
        'error_heading': (By.CSS_SELECTOR, 'h2#error'),
    }

    def __init__(self, driver, goto=True, require_login=False):
        super(OSFBasePage, self).__init__(driver)
        if require_login:
            login(self)

        if goto:
            driver.get(self.url)

        # Verify the page is what you expect it to be.
        if not self.verify():
            url = driver.current_url

            # If we've got an error message here, grab it
            try:
                if self.error_heading:
                    raise HttpError(
                        driver=self.driver,
                        code=self.error_heading.get_attribute('data-http-status-code'),
                    )
            except ValueError:
                pass

            raise PageException('Unexpected page structure: `{}`'.format(
                url
            ))

        self.navbar = self.BasePageNavbar(driver)

    def verify(self):
        try:
            self.identity
        except ValueError:
            return False
        else:
            return True

    def is_logged_in(self):
        return self.navbar.is_logged_in()

    class BasePageNavbar(Navbar):

        locators = {
            **Navbar.locators,
            **{
                'my_project_link': (By.CSS_SELECTOR, '#secondary-navigation > ul > li:nth-last-child(5) > a'),
            }
        }

        def verify(self):
            return self.current_service.text == 'HOME'
