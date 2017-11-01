import settings
from pages.base import OSFBasePage, Navbar
from selenium.webdriver.common.by import By


class PreprintPage(OSFBasePage):
    url = settings.OSF_HOME + '/preprints'

    locators = {
        'add_preprint': (By.CSS_SELECTOR, 'div.preprint-page div.preprint-header div.container div div a[href="/preprints/submit"]', settings.LONG_TIMEOUT),
    }

    def __init__(self, driver, goto=True):
        super(PreprintPage, self).__init__(driver, goto)
        self.navbar = self.PreprintPageNavbar(driver)

    def verify_page(self):
        return len(self.driver.find_elements(By.CSS_SELECTOR, 'div.preprints-page div.preprint-header')) == 1

    class PreprintPageNavbar(Navbar):

        locators = dict(
            add_a_preprint_link=(By.XPATH, '//nav[@id="navbarScope"]/div/div[@class="navbar-header"]/div[@class="dropdown"]/ul[@role="menu"]/li/a[@href="' + settings.OSF_HOME + '/meetings/"]'),
            **Navbar.locators
        )

        def verify(self):
            return self.current_service.text == 'PREPRINTS'
