import settings

from pages.base import OSFBasePage, Navbar
from selenium.webdriver.common.by import By


class PreprintPage(OSFBasePage):
    url = settings.OSF_HOME + '/preprints'

    locators = {
        'identity': (By.CSS_SELECTOR, 'body.ember-application > div.ember-view > div.preprints-page > div.preprint-header', settings.LONG_TIMEOUT),
        'add_preprint_link': (By.CSS_SELECTOR, 'div.preprint-page div.preprint-header div.container div div a[href="/preprints/submit"]', settings.LONG_TIMEOUT),
    }

    def __init__(self, driver, verify=False):
        super(PreprintPage, self).__init__(driver, verify)
        self.navbar = self.PreprintPageNavbar(driver)

    class PreprintPageNavbar(Navbar):

        locators = {
            **Navbar.locators,
            **{
                'add_a_preprint_link': (By.CSS_SELECTOR, '#secondary-navigation > ul > li:nth-last-child(5) > a'),
                'user_dropdown': (By.CSS_SELECTOR, '#secondary-navigation > ul > li:nth-last-of-type(1) > a'),
            }
        }

        def verify(self):
            return self.current_service.text == 'PREPRINTS'

        @property
        def sign_in_button(self):
            return self.second_navigation.find_element(
                By.CSS_SELECTOR,
                'ul.nav > li.ember-view.dropdown.sign-in > a.btn.btn-info.btn-top-login'
            )
