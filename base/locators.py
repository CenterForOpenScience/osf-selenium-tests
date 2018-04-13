import settings

from base import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException

class WebElementWrapper:

    def __init__(self, driver, attribute_name, locator):
        self.driver = driver
        self.locator = locator
        self.name = attribute_name

    def __getattr__(self, item):
        return getattr(self.element, item)

    @property
    def element(self):
        return self.locator.get_web_element(self.driver, self.name)

    def present(self):
        try:
            self.element
            return True
        except ValueError:
            return False

    def absent(self, timeout=settings.QUICK_TIMEOUT):
        """
        Boolean to check if an element is no longer visible on a page.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(self.locator.location)
            )
            return True
        except TimeoutException:
            return False

    def here_then_gone(self):
        self.present()  # Allow a wait for it to appear, but don't force it to have been present
        if not self.absent():
            raise ValueError('Element {} is not absent.'.format(self.name))
        return True

    def click_expecting_popup(self, timeout=settings.TIMEOUT):
        og_window = self.driver.current_window_handle

        for window in self.driver.window_handles:
            if window == og_window:
                continue
            self.driver.switch_to.window(window)
            self.driver.close()

        self.driver.switch_to.window(og_window)
        self.driver.maximize_window()
        self.click()

        try:
            WebDriverWait(self.driver, timeout).until(
                EC.number_of_windows_to_be(2))
        except TimeoutException:
            raise ValueError('No new window was opened.')
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.maximize_window()


class BaseLocator:

    def __init__(self, selector, path, timeout=settings.TIMEOUT):
        self.selector = selector
        self.path = path
        self.location = (selector, path)
        self.timeout = timeout

    def get_element(self, driver, attribute_name):
        raise NotImplementedError


class Locator(BaseLocator):

    def get_web_element(self, driver, attribute_name):
        """
        Checks if element is on page, visible, and clickable before returning the selenium webElement.

        This method is adapted from code provided on seleniumframework.com
        """
        try:
            WebDriverWait(driver, self.timeout).until(
                EC.presence_of_element_located(self.location)
            )
        except(TimeoutException, StaleElementReferenceException):
            raise ValueError('Element {} not present on page. {}'.format(
                attribute_name, driver.current_url)) from None

        try:
            WebDriverWait(driver, self.timeout).until(
                EC.visibility_of_element_located(self.location)
            )
        except(TimeoutException, StaleElementReferenceException):
            raise ValueError('Element {} not visible before timeout. {}'.format(
                attribute_name, driver.current_url)) from None

        if 'href' in attribute_name:
            try:
                WebDriverWait(driver, self.timeout).until(
                    ec.link_has_href(self.location)
                )
            except(TimeoutException, StaleElementReferenceException):
                raise ValueError('Element {} on page but does not have a href. {}'.format(
                    attribute_name, driver.current_url)) from None
        try:
            return driver.find_element(self.selector, self.path)
        except NoSuchElementException:
            raise ValueError('Element {} was present, but now is gone. {}'.format(
                attribute_name, driver.current_url)) from None

    def get_element(self, driver, attribute_name):
        return WebElementWrapper(driver, attribute_name, self)


class GroupLocator(BaseLocator):
    def get_web_elements(self, driver):
        return driver.find_elements(self.selector, self.path)

    def get_element(self, driver, attribute_name=None):
        return self.get_web_elements(driver)


class ComponentLocator(Locator):

    def __init__(self, component_class, selector=None, path=None, timeout=settings.TIMEOUT):
        super().__init__(selector, path, timeout)
        self.component_class = component_class

    def get_element(self, driver, attribute_name=None):
        return self.component_class(driver)


class BaseElement:
    default_timeout = settings.TIMEOUT

    def __new__(cls, *args, **kwargs):
        page = super().__new__(cls)
        if hasattr(cls, 'waffle_override'):
            for waffle_name in cls.waffle_override:
                if waffle_name in settings.EMBER_PAGES:
                    page = super().__new__(cls.waffle_override[waffle_name])
        page.__init__(*args, **kwargs)
        return page

    def __init__(self, driver):
        self.driver = driver

    def verify(self):
        raise NotImplementedError

    def __getattribute__(self, attribute_name):
        value = object.__getattribute__(self, attribute_name)
        if isinstance(value, BaseLocator):
            return value.get_element(self.driver, attribute_name)
        return value
