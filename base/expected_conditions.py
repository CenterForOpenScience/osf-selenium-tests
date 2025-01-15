from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC


class link_has_href(object):
    """An Expectation for checking link is visible and has an href so
    you can click it."""

    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element_href = EC._find_element(driver, self.locator).get_attribute('href')
        if element_href:
            return element_href
        else:
            return False


class window_at_index(object):
    """An Expectation for checking if a tab is open for certain index
    so you can switch to it."""

    def __init__(self, page_index):
        self.page_index = page_index

    def __call__(self, driver):
        return len(driver.window_handles) > self.page_index


class text_to_be_present_in_elements(object):
    """ An expectation for checking if the given text is present in the
    specified element.
    locator, text
    """
    def __init__(self, locator, text_):
        self.locator = locator
        self.text = text_

    def __call__(self, driver: WebDriver):
        try:
            element_texts = [element.text for element in driver.find_elements(*self.locator)]
            return any([self.text in element_text for element_text in element_texts])
        except StaleElementReferenceException:
            return False