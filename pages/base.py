import settings

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException

from pages.exceptions import HttpError, PageException, LoginError


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
                raise ValueError('Element {} not present on page. {}'.format(element, self.driver.current_url))

            try:
                WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located(location)
                )
            except(TimeoutException, StaleElementReferenceException):
                raise ValueError('Element {} not visible before timeout. {}'.format(element, self.driver.current_url))

            if 'link' in element:
                try:
                    WebDriverWait(self.driver, timeout).until(
                        EC.element_to_be_clickable(location)
                    )
                except(TimeoutException, StaleElementReferenceException):
                    raise ValueError('Element {} on page but not clickable. {}'.format(element, self.driver.current_url))

            return self.find_element(*location)
        else:
            raise ValueError('Cannot find element {}. {}'.format(element, self.driver.current_url))


class BasePage(BaseElement):
    url = None

    def goto(self):
        self.driver.get(self.url)
        self.check_page()

    def check_page(self):
        if not self.verify():
            # handle any specific kind of error before go to page exception
            self.error_handling()
            raise PageException('Unexpected page structure: `{}` with identity {}'.format(
                self.driver.current_url, self.locators['identity']
            ))

    def verify(self):
        try:
            self.identity
        except ValueError:
            return False
        else:
            return True

    def error_handling(self):
        pass

    def reload(self):
        self.driver.refresh()


class Navbar(BaseElement):

    locators = {
        'service_dropdown': (By.CSS_SELECTOR, '#navbarScope > div.container > div.navbar-header > div.dropdown > button'),
        'home_link': (By.CSS_SELECTOR, '#navbarScope > div.container > div.navbar-header > div.dropdown > ul > li:nth-child(1) > a'),
        'preprints_link': (By.CSS_SELECTOR, '#navbarScope > div.container > div.navbar-header > div.dropdown > ul > li:nth-child(2) > a'),
        'registries_link': (By.CSS_SELECTOR, '#navbarScope > div.container > div.navbar-header > div.dropdown > ul > li:nth-child(3) > a'),
        'meetings_link': (By.CSS_SELECTOR, '#navbarScope > div.container > div.navbar-header > div.dropdown > ul > li:nth-child(4) > a'),
        'search_link':(By.ID, 'navbar-search'),
        'support_link': (By.ID, 'navbar-support'),
        'donate_link': (By.ID, 'navbar-donate'),
        'user_dropdown': (By.CSS_SELECTOR, '#secondary-navigation > ul > li:nth-last-of-type(1) > button'),
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
            if self.sign_up_button:
                return False
        except ValueError:
            return True


class LoginPage(BasePage):
    url = settings.OSF_HOME + '/login'

    locators = {
        'identity': (By.XPATH, '/html/body[@id="cas"]/div[@id="container"]', settings.LONG_TIMEOUT),
        'username_input': (By.ID, 'username'),
        'password_input': (By.ID, 'password'),
        'submit_button': (By.NAME, 'submit'),
        'remember_me_checkbox': (By.ID, 'rememberMe'),
    }

    if 'localhost:5000' in settings.OSF_HOME:
        locators['submit_button'] = (By.ID, 'submit')
        locators['identity'] = (By.ID, 'login')

    def __init__(self, driver, verify=False):
        super(LoginPage, self).__init__(driver)
        if verify:
            self.check_page()

    def error_handling(self):
        if self.url not in self.driver.current_url:
            raise LoginError(
                driver=self.driver,
                error_info='Already logged in'
            )

    def login(self, user, password):
        self.username_input.send_keys(user)
        if ('localhost:5000'  not in settings.OSF_HOME):
            self.password_input.send_keys(password)
            if self.remember_me_checkbox.is_selected():
                self.remember_me_checkbox.click()
        self.submit_button.click()


def login(osf_page, user=settings.USER_ONE, password=settings.USER_ONE_PASSWORD):
    login_page = LoginPage(osf_page.driver)
    login_page.goto()
    login_page.login(user, password)
    osf_page.driver.get(osf_page.url)


class OSFBasePage(BasePage):
    url = settings.OSF_HOME

    # all page must have unique identity
    locators = {}

    def __init__(self, driver, verify=False, require_login=False):
        super(OSFBasePage, self).__init__(driver)

        self.navbar = self.BasePageNavbar(driver)

        if require_login:
            self.driver.get(self.url)
            if not self.is_logged_in():
                login(self)

        if verify:
            self.check_page()

    @property
    def error_heading(self):
        try:
            error_head = self.find_element(By.CSS_SELECTOR, 'h2#error')
        except NoSuchElementException:
            return None
        else:
            return error_head.text

    def error_handling(self):
        # If we've got an error message here, grab it
        if self.error_heading:
            raise HttpError(
                driver=self.driver,
                code=self.error_heading.get_attribute('data-http-status-code'),
            )


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
