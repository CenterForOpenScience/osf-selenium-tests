import settings

from pages.base import OSFBasePage, Navbar
from selenium.webdriver.common.by import By


class RegistriesPage(OSFBasePage):
    url = settings.OSF_HOME + '/registries'

    locators = {
        'identity': (By.CSS_SELECTOR, 'body.ember-application > div.ember-view > div.preprints-page > div.search-header > div.container > div.row > div > div.registries-brand', settings.LONG_TIMEOUT),
    }

    def __init__(self, driver, verify=False):
        super(RegistriesPage, self).__init__(driver, verify)
        self.navbar = self.RegistriesPageNavbar(driver)

    class RegistriesPageNavbar(Navbar):

        locators = {
            **Navbar.locators,
            **{
                'user_dropdown': (By.CSS_SELECTOR, '#secondary-navigation > ul > li:nth-last-of-type(1) > a'),
                'second_navigation': (By.ID, 'secondary-navigation')
            }
        }

        def verify(self):
            return self.current_service.text == 'REGISTRIES'

        @property
        def sign_in_button(self):
            return self.second_navigation.find_element(
                By.CSS_SELECTOR,
                'ul.nav > li.ember-view.dropdown.sign-in > a.btn.btn-info.btn-top-login'
            )