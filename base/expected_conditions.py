from selenium.webdriver.support import expected_conditions as EC

class link_has_href(object):
    """ An Expectation for checking link is visible and has an href so
    you can click it."""
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element = EC.visibility_of_element_located(self.locator)(driver)
        if element and element.get_property('href'):
            return element
        else:
            return False
