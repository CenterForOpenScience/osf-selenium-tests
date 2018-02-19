import settings

from pages.base import OSFBasePage, Navbar, Locator
from selenium.webdriver.common.by import By


class BasePreprintPage(OSFBasePage):

    def __init__(self, driver, verify=False):
        super(BasePreprintPage, self).__init__(driver, verify)
        self.navbar = self.PreprintPageNavbar(driver)

    class PreprintPageNavbar(Navbar):

        # Locators
        add_a_preprint_link = Locator(By.CSS_SELECTOR, '#secondary-navigation > ul > li:nth-last-child(5) > a')
        user_dropdown = Locator(By.CSS_SELECTOR, '#secondary-navigation > ul > li:nth-last-of-type(1) > a')
        sign_in_button = Locator(By.CSS_SELECTOR, '#secondary-navigation > ul.nav > li.ember-view.dropdown.sign-in > a.btn.btn-info.btn-top-login', settings.LONG_TIMEOUT)

        def verify(self):
            return self.current_service.text == 'PREPRINTS'

class PreprintPage(BasePreprintPage):
    url = settings.OSF_HOME + '/preprints/'

    # Locators
    identity = Locator(By.CSS_SELECTOR, 'body.ember-application > div.ember-view > div.preprints-page > div.preprint-header', settings.LONG_TIMEOUT)
    add_preprint_link = Locator(By.CSS_SELECTOR, 'div.preprint-page div.preprint-header div.container div div a[href="/preprints/submit"]', settings.LONG_TIMEOUT)


class SubmitPreprintPage(BasePreprintPage):
    url = settings.OSF_HOME + '/preprints/submit/'

    # Locators
    identity = Locator(By.CSS_SELECTOR, 'div.preprint-submit-header')
