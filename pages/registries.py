import settings
from pages.base import OSFBasePage, Navbar
from selenium.webdriver.common.by import By


class RegistriesPage(OSFBasePage):
    url = settings.OSF_HOME + '/registries'

    locators = {
        **OSFBasePage.locators,
        **{
            'identity': (By.CSS_SELECTOR, 'body.ember-application > div.ember-view > div.preprints-page > div.search-header > div.container > div.row > div > div.registries-brand', settings.LONG_TIMEOUT),
            'user_dropdown': (By.CSS_SELECTOR, '#secondary-navigation > ul > li:nth-last-of-type(1) > a'),
        }
    }

    def __init__(self, driver, goto=True):
        super(RegistriesPage, self).__init__(driver, goto)
        self.navbar = self.RegistriesPageNavbar(driver)

    class RegistriesPageNavbar(Navbar):

        def verify(self):
            return self.current_service.text == 'REGISTRIES'
