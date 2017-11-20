import settings

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException

from pages.exceptions import HttpError, PageException, LoginError

class Locator:

    def __init__(self, selector, path, timeout=settings.TIMEOUT):
        self.selector = selector
        self.path = path
        self.location = (selector, path)
        self.timeout = timeout

    def get_web_element(self, driver, element):
        """
        Checks if elements are on page, visible, and clickable before returning the selenium webElement.

        This method is adapted from code provided on seleniumframework.com
        """

        try:
            WebDriverWait(driver, self.timeout).until(
                EC.presence_of_element_located(self.location)
            )
        except(TimeoutException, StaleElementReferenceException):
            raise ValueError('Element {} not present on page. {}'.format(element, driver.current_url))

        try:
            WebDriverWait(driver, self.timeout).until(
                EC.visibility_of_element_located(self.location)
            )
        except(TimeoutException, StaleElementReferenceException):
            raise ValueError('Element {} not visible before timeout. {}'.format(element, driver.current_url))

        if 'link' in element:
            try:
                WebDriverWait(driver, self.timeout).until(
                    EC.element_to_be_clickable(self.location)
                )
            except(TimeoutException, StaleElementReferenceException):
                raise ValueError('Element {} on page but not clickable. {}'.format(element, driver.current_url))

        return driver.find_element(self.selector, self.path)


class BaseElement:
    default_timeout = settings.TIMEOUT

    def __init__(self, driver):
        self.driver = driver

    def verify(self):
        raise NotImplementedError

    def __getattribute__(self, item):
        value = object.__getattribute__(self, item)
        if type(value) is Locator:
            return value.get_web_element(self.driver, item)
        return value


class BasePage(BaseElement):
    url = None

    def goto(self):
        self.driver.get(self.url)
        self.check_page()

    def check_page(self):
        if not self.verify():
            # handle any specific kind of error before go to page exception
            self.error_handling()
            raise PageException('Unexpected page structure: `{}`'.format(self.driver.current_url))  # TODO: Add locator information here

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
    service_dropdown = Locator(By.CSS_SELECTOR, '#navbarScope > div.container > div.navbar-header > div.dropdown > button')
    home_link = Locator(By.CSS_SELECTOR, '#navbarScope > div.container > div.navbar-header > div.dropdown > ul > li:nth-child(1) > a')
    preprints_link = Locator(By.CSS_SELECTOR, '#navbarScope > div.container > div.navbar-header > div.dropdown > ul > li:nth-child(2) > a')
    registries_link = Locator(By.CSS_SELECTOR, '#navbarScope > div.container > div.navbar-header > div.dropdown > ul > li:nth-child(3) > a')
    meetings_link = Locator(By.CSS_SELECTOR, '#navbarScope > div.container > div.navbar-header > div.dropdown > ul > li:nth-child(4) > a')
    search_link = Locator(By.ID, 'navbar-search')
    support_link = Locator(By.ID, 'navbar-support')
    donate_link = Locator(By.ID, 'navbar-donate')
    user_dropdown = Locator(By.CSS_SELECTOR, '#secondary-navigation > ul > li:nth-last-of-type(1) > button')
    user_dropdown_profile = Locator(By.CSS_SELECTOR, '#secondary-navigation > ul > li.dropdown.open > ul > li:nth-child(1) > a')
    user_dropdown_support = Locator(By.CSS_SELECTOR, '#secondary-navigation > ul > li.dropdown.open > ul > li:nth-child(2) > a')
    user_dropdown_settings = Locator(By.CSS_SELECTOR, '#secondary-navigation > ul > li.dropdown.open > ul > li:nth-child(3) > a')
    sign_up_button = Locator(By.LINK_TEXT, 'Sign Up')
    sign_in_button = Locator(By.LINK_TEXT, 'Sign In')
    logout_link = Locator(By.CSS_SELECTOR, '#secondary-navigation > ul > li.dropdown.open > ul > li:nth-child(4) > a')
    current_service = Locator(By.CSS_SELECTOR, '#navbarScope > div > div > div.service-home > a > span.current-service > strong')

    def verify(self):
        return len(self.driver.find_elements(By.ID, 'navbarScope')) == 1

    def is_logged_in(self):
        try:
            if self.sign_up_button:
                return False
        except ValueError:
            return True


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
        if ('localhost:5000' not in settings.OSF_HOME):
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

    # all page must have a unique identity

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
        # If we've got an error message here from osf, grab it
        if self.error_heading:
            raise HttpError(
                driver=self.driver,
                code=self.error_heading.get_attribute('data-http-status-code'),
            )

    def is_logged_in(self):
        return self.navbar.is_logged_in()

    class BasePageNavbar(Navbar):

        # Locators
        my_project_link = Locator(By.CSS_SELECTOR, '#secondary-navigation > ul > li:nth-last-child(5) > a')

        def verify(self):
            return self.current_service.text == 'HOME'
