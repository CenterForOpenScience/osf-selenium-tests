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

    def open(self):
        self.driver.get(self.url)

class OSFBasePage(BasePage):
    url = settings.DOMAIN

    def __init__(self, driver):
        super(OSFBasePage, self).__init__(driver)
        self.navbar = self.Navbar(driver)

    locator_dictionary = {
        'sign_in_button': (By.LINK_TEXT, 'Sign In')
    }

    def is_logged_in(self):
        return self.navbar.logged_in()


    class Navbar(BaseElement):

        locator_dictionary = {
            'sign_in_button': (By.LINK_TEXT, 'Sign In'),
            'username_input': (By.ID, 'username'),
            'password_input': (By.ID, 'password'),
            'submit_button': (By.NAME, 'submit'),
            'local_submit_button': (By.ID, 'submit'),
            'remember_me_checkbox': (By.ID, 'rememberMe'),
            'user_dropdown': (By.CSS_SELECTOR, '#secondary-navigation > ul > li:nth-child(5) > button'),
            'logout_link': (By.CSS_SELECTOR, '#secondary-navigation > ul > li.dropdown.open > ul > li:nth-child(4) > a')
        }

        def logged_in(self):
            try:
                if self.sign_in_button:
                    return False
            except:
                return True

        def login(self):
            if not self.logged_in():
                self.sign_in_button.click()
                self.username_input.send_keys(settings.USERNAME_ONE)
                if ("localhost:5000" in settings.DOMAIN):
                    self.local_submit_button.click()
                else:
                    self.password_input.send_keys(settings.PASSWORD)
                    if self.remember_me_checkbox.is_selected():
                        self.remember_me_checkbox.click()
                    self.submit_button.click()

        def logout(self):
            if self.logged_in():
                self.user_dropdown.click()
                self.logout_link.click()
