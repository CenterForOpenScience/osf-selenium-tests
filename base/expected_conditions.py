from selenium.webdriver.support import expected_conditions as EC


class link_has_href(object):
    """ An Expectation for checking link is visible and has an href so
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
    """ An Expectation for checking if a tab is open for certain index
    so you can switch to it."""
    def __init__(self, page_index):
        self.page_index = page_index

    def __call__(self, driver):
        return len(driver.window_handles) > self.page_index


class correct_keys_sent(object):
    """ An Exception used for checking if the correct keys have been sent to an input.
    This is used for repeatedly attempting to send keys to IE because sometimes it sends the
    incorrect keys.

    Note: This is not a great example of an expected condition because it changes what's on the page.
    """
    def __init__(self, element, keys, existing_keys):
        self.element = element
        self.keys = keys
        self.correct_keys = existing_keys + keys

    def __call__(self, driver):

        if self.element.get_attribute('value') == self.correct_keys:
            return True
        else:
            self.element.clear()
            self.element.send_keys(self.correct_keys)
            return False
