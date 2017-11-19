import settings

from selenium.webdriver.common.by import By
from pages.base import OSFBasePage, Navbar, Locator


class RegistriesPage(OSFBasePage):
    url = settings.OSF_HOME + '/registries'

    # Locators
    identity = Locator(By.CSS_SELECTOR, 'body.ember-application > div.ember-view > div.preprints-page > div.search-header > div.container > div.row > div > div.registries-brand', settings.LONG_TIMEOUT)

    def __init__(self, driver, verify=False):
        super(RegistriesPage, self).__init__(driver, verify)
        self.navbar = self.RegistriesPageNavbar(driver)

    class RegistriesPageNavbar(Navbar):

        # Locators
        user_dropdown = Locator(By.CSS_SELECTOR, '#secondary-navigation > ul > li:nth-last-of-type(1) > a')
        sign_in_button = Locator(By.CSS_SELECTOR, '#secondary-navigation > ul.nav > li.ember-view.dropdown.sign-in > a.btn.btn-info.btn-top-login', settings.LONG_TIMEOUT)

        def verify(self):
            return self.current_service.text == 'REGISTRIES'
