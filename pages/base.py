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

    def __getattr__(self, what):
        """
        This method is adapted from code provided on seleniumframework.com
        """
        timeout = self.default_timeout

        if what in self.locator_dictionary.keys():
            if len(self.locator_dictionary[what]) == 3:
                timeout = self.locator_dictionary[what][2]
            location = (self.locator_dictionary[what][0], self.locator_dictionary[what][1])

            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(location)
                )
            except(TimeoutException,StaleElementReferenceException):
                raise ValueError('Element {} not present on page'.format(what))

            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located(location)
                )
            except(TimeoutException,StaleElementReferenceException):
                raise ValueError('Element {} not visible before timeout'.format(what))
            # I could have returned element, however because of lazy loading, I am seeking the element before return
            return self.find_element(*location)
        else:
            raise ValueError('Cannot find element {}'.format(what))

class BasePage(BaseElement):
    url = None

    def goto(self):
        self.driver.get(self.url)

    def verify_page(self):
        """
        Use an element from the locator_dictionary to check if we're on expected page
        """
        try:
            self.__getattr__(list(self.locator_dictionary.keys())[0])
            return True
        except (TimeoutException,StaleElementReferenceException):
            return False

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

        locator_dictionary = {
            'sign_in_button': (By.LINK_TEXT, 'Sign In'),
            'user_dropdown': (By.CSS_SELECTOR, '#secondary-navigation > ul > li:nth-child(5) > button'),
            'logout_link': (By.CSS_SELECTOR, '#secondary-navigation > ul > li.dropdown.open > ul > li:nth-child(4) > a')
        }

        def is_logged_in(self):
            try:
                if self.sign_in_button:
                    return False
            except:
                return True
