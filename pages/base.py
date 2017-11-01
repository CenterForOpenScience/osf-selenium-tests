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
        'home_link': (By.XPATH, '//nav[@id="navbarScope"]/div/div[@class="navbar-header"]/div[@class="dropdown"]/ul[@role="menu"]/li/a[@href="' + settings.OSF_HOME + '"]'),
        'preprint_link': (By.XPATH, '//nav[@id="navbarScope"]/div/div[@class="navbar-header"]/div[@class="dropdown"]/ul[@role="menu"]/li/a[@href="' + settings.OSF_HOME + '/preprints/"]'),
        'registries_link': (By.XPATH, '//nav[@id="navbarScope"]/div/div[@class="navbar-header"]/div[@class="dropdown"]/ul[@role="menu"]/li/a[@href="' + settings.OSF_HOME + '/registries/"]'),
        'meetings_link': (By.XPATH, '//nav[@id="navbarScope"]/div/div[@class="navbar-header"]/div[@class="dropdown"]/ul[@role="menu"]/li/a[@href="' + settings.OSF_HOME + '/meetings/"]'),
        'search_link': (By.XPATH, '//div[@id="secondary-navigation"]/ul/li/a[@href="' + settings.OSF_HOME + '/search/"]'),
        'support_link': (By.XPATH, '//div[@id="secondary-navigation"]/ul/li/a[@href="/support/"]'),
        'donate_link': (By.XPATH, '//div[@id="secondary-navigation"]/ul/li/a[@href="https://cos.io/donate"]'),
        'user_dropdown': (By.CSS_SELECTOR, '#secondary-navigation > ul > li:nth-child(5) > button'),
        'user_dropdown_profile': (By.XPATH, '//div[@id="secondary-navigation"]/ul/li[@class="dropdown"]/ul/li/a[@href="/logout/"]'),
        'user_dropdown_support': (By.XPATH, '//div[@id="secondary-navigation"]/ul/li[@class="dropdown"]/ul/li/a[@href="' + settings.OSF_HOME + '/support/"]'),
        'user_dropdown_settings': (By.XPATH, '//div[@id="secondary-navigation"]/ul/li[@class="dropdown"]/ul/li/a[@href="/settings/"]'),
        'sign_up_button': (By.LINK_TEXT, 'Sign Up'),
        'sign_in_button': (By.LINK_TEXT, 'Sign In'),
        'logout_link': (By.CSS_SELECTOR, '#secondary-navigation > ul > li.dropdown.open > ul > li:nth-child(4) > a'),
        'current_service': (By.CSS_SELECTOR, '#navbarScope > div > div > div.service-home > a > span.current-service > strong')
    }

    def __init__(self, driver):
        super(Navbar, self).__init__(driver)

    def verify(self):
        return len(self.find_elements(By.XPATH, '//nav[@id="navbarScope"]')) == 1

    def is_logged_in(self):
        try:
            if self.sign_in_button:
                return False
        except ValueError:
            return True


class OSFBasePage(BasePage):
    url = settings.OSF_HOME

    locators = {
        'error_heading':(By.CSS_SELECTOR, 'h2#error')
    }

    def __init__(self, driver, goto=True):
        super(OSFBasePage, self).__init__(driver)
        if goto:
            # Verify the page is what you expect it to be.
            driver.get(self.url)

        if not self.verify():
            url = driver.current_url

            # If we've got an error message here, grab it
            try:
                if self.error_heading:
                    raise HttpError(
                        driver=self.driver,
                        code=self.error_heading.get_attribute('data-http-status-code'),
                    )
            except(TimeoutException, StaleElementReferenceException):
                pass

            raise PageException('Unexpected page structure: `{}`'.format(
                url
            ))

        self.navbar = self.BasePageNavbar(driver)

    def verify(self):
        return True

    def is_logged_in(self):
        return self.navbar.is_logged_in()

    class BasePageNavbar(Navbar):

        locators = dict(
            my_project_link=(By.XPATH, '//div[@id="secondary-navigation"]/ul/li/a[@href="' + settings.OSF_HOME + '/myprojects/"]'),
            **Navbar.locators
        )

        def verify(self):
            return self.current_service.text == 'HOME'
