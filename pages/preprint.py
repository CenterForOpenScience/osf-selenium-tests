import settings
from pages.base import OSFBasePage, Navbar
from selenium.webdriver.common.by import By


class PreprintPage(OSFBasePage):
    url = settings.OSF_HOME + '/preprints'

    locators = dict(
        add_preprint=(By.CSS_SELECTOR, 'div.preprint-page div.preprint-header div.container div div a[href="/preprints/submit"]', settings.LONG_TIMEOUT),
        identity=(By.CSS_SELECTOR, '#ember680 > div.preprint-page > div.preprint-header', settings.LONG_TIMEOUT),
        **OSFBasePage.locators
    )

    def __init__(self, driver, goto=True):
        super(PreprintPage, self).__init__(driver, goto)
        self.navbar = self.PreprintPageNavbar(driver)

    class PreprintPageNavbar(Navbar):

        locators = dict(
            add_a_preprint_link=(By.CSS_SELECTOR, '#secondary-navigation > ul > li:nth-child(1) > a'),
            **Navbar.locators
        )

        def verify(self):
            return self.current_service.text == 'PREPRINTS'
