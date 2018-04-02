import settings

import urllib.parse
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from components.navbars import HomeNavbar
from base.locators import BaseElement, ComponentLocator
from base.exceptions import HttpError, PageException


class BasePage(BaseElement):
    url = None

    def __init__(self, driver, verify=False):
        super().__init__(driver)
        if verify:
            self.check_page()

    def goto(self):
        self.driver.get(self.url)
        self.check_page()

    def check_page(self):
        if not self.verify():
            # handle any specific kind of error before go to page exception
            self.error_handling()
            raise PageException('Unexpected page structure: `{}`'.format(self.driver.current_url))

    def verify(self):
        return self.identity.present()

    def error_handling(self):
        pass

    def reload(self):
        self.driver.refresh()

    def scroll_into_view(self, element):
        self.driver.execute_script('arguments[0].scrollIntoView(false);', element)
        # Account for navbar
        self.driver.execute_script('window.scrollBy(0, 55)')

    def drag_and_drop(self, source_element, dest_element):
        source_element.click()
        ActionChains(self.driver).drag_and_drop(source_element, dest_element).perform()
        # Note: If you close the browser too quickly, the drag/drop may not go through


class OSFBasePage(BasePage):
    url = settings.OSF_HOME
    navbar = ComponentLocator(HomeNavbar)
    # all pages must have a unique identity or overwrite verify

    def __init__(self, driver, verify=False):
        super().__init__(driver)

        if verify:
            self.check_page()

    @property
    def error_heading(self):
        try:
            error_head = self.driver.find_element(By.CSS_SELECTOR, 'h2#error')
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

    def is_logged_out(self):
        return self.navbar.is_logged_out()


class GuidBasePage(OSFBasePage):
    def __init__(self, driver, verify=False, guid=None):
        super().__init__(driver, verify)
        self.url = urllib.parse.urljoin(settings.OSF_HOME, guid) if guid else None
