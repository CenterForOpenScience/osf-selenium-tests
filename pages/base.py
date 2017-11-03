import settings

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException


class BaseElement(object):
    default_timeout = settings.TIMEOUT

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, *loc):
        return self.driver.find_element(*loc)

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

    def verify_page(self):
        raise NotImplementedError

    def reload(self):
        self.driver.refresh()

class OSFBasePage(BasePage):
    url = settings.OSF_HOME

    def __init__(self, driver):
        super(OSFBasePage, self).__init__(driver)
        self.navbar = self.Navbar(driver)

    def is_logged_in(self):
        return self.navbar.is_logged_in()

    class Navbar(BaseElement):

        locators = {
            'sign_in_button': (By.LINK_TEXT, 'Sign In'),
            'user_dropdown': (By.CSS_SELECTOR, '#secondary-navigation > ul > li:nth-child(5) > button'),
            'logout_link': (By.CSS_SELECTOR, '#secondary-navigation > ul > li.dropdown.open > ul > li:nth-child(4) > a')
        }

        def is_logged_in(self):
            try:
                if self.sign_in_button:
                    return False
            except ValueError:
                return True
