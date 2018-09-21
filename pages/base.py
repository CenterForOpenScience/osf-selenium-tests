import settings

import urllib.parse
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from components.navbars import HomeNavbar
from base.locators import BaseElement, ComponentLocator, Locator
from base.exceptions import HttpError, PageException


class BasePage(BaseElement):
    url = None

    cas_identity = Locator(By.ID, 'cas')

    def __init__(self, driver, verify=False):
        super().__init__(driver)

        if verify:
            self.check_page()

    def goto(self, expect_login_redirect=False):
        """Navigate to a page based on its `url` attribute
        and confirms you are on the expected page.

        If you are testing permissions, you may want to navigate to a page that
        requires authentication as a logged out user. In this case you will be
        redirected to CAS. You can set `expect_login_redirect` to True to verify
        you are on the login page.
        """
        self.driver.get(self.url)
        if expect_login_redirect:

            current_url = self.driver.current_url
            if not (self.cas_identity.present() and self.url in current_url):
                raise PageException('Unexpected page structure: `{}`'.format(self.driver.current_url))
        else:
            self.check_page()

    def check_page(self):
        if not self.verify():
            # handle any specific kind of error before go to page exception
            self.error_handling()
            raise PageException('Unexpected page structure: `{}`'.format(self.driver.current_url))

    def verify(self):
        """Verify that you are on the expected page by confirming the page's `identity`
        element is present on the page.
        """
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

    def click_recaptcha(self):
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name('iframe'))
        self.driver.find_element_by_css_selector('.recaptcha-checkbox-checkmark').click()
        self.driver.switch_to.default_content()
        #TODO: Replace with an expected condition that checks if aria-checked="true"
        sleep(1)

class OSFBasePage(BasePage):
    """
    Note: All pages must have a unique identity or overwrite `verify`
    """
    url = settings.OSF_HOME
    navbar = ComponentLocator(HomeNavbar)

    def __init__(self, driver, verify=False):
        super().__init__(driver, verify)

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
            raise HttpError(self.error_heading.get_attribute('data-http-status-code'))

    def is_logged_in(self):
        return self.navbar.is_logged_in()

    def is_logged_out(self):
        return self.navbar.is_logged_out()


class GuidBasePage(OSFBasePage):
    base_url = urllib.parse.urljoin(settings.OSF_HOME, '{guid}')
    guid = ''

    def __init__(self, driver, verify=False, guid='', domain=settings.OSF_HOME):
        super().__init__(driver, verify)
        # self.domain = domain
        self.guid = guid

    @property
    def url(self):
        if '{guid}' in self.base_url:
            return self.base_url.format(guid=self.guid)
        else:
            raise ValueError('No space in base_url for GUID specified.')
