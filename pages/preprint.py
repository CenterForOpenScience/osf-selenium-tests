import settings
from pages.base import OSFBasePage, Navbar
from selenium.webdriver.common.by import By


class PreprintPage(OSFBasePage):
    url = settings.OSF_HOME + '/preprints'

    locators = {
        **OSFBasePage.locators,
        **{
            'identity': (By.CSS_SELECTOR, 'body.ember-application > div.ember-view > div.preprints-page > div.preprint-header', settings.LONG_TIMEOUT),
            'add_preprint_link': (By.CSS_SELECTOR, 'div.preprint-page div.preprint-header div.container div div a[href="/preprints/submit"]', settings.LONG_TIMEOUT),
        }
    }

    def __init__(self, driver, goto=True):
        super(PreprintPage, self).__init__(driver, goto)
        self.navbar = self.PreprintPageNavbar(driver)

    class PreprintPageNavbar(Navbar):

        locators = {
            **Navbar.locators,
            **{
                'add_a_preprint_link': (By.CSS_SELECTOR, '#secondary-navigation > ul > li:nth-last-child(5) > a'),
                'search_link': (By.XPATH, '/html/body/div[@class="ember-view]/div[1]/nav[@id="navbarScope"]/div[@class="container"]/div[@id="secondary-navigation"]/ul/li[2]/a'),
                'support_link': (By.XPATH, '/html/body/div[@class="ember-view]/div[1]/nav[@id="navbarScope"]/div[@class="container"]/div[@id="secondary-navigation"]/ul/li[3]/a'),
                'donate_link': (By.XPATH, '/html/body/div[@class="ember-view]/div[1]/nav[@id="navbarScope"]/div[@class="container"]/div[@id="secondary-navigation"]/ul/li[4]/a'),
                'user_dropdown': (By.CSS_SELECTOR, '#secondary-navigation > ul > li:nth-last-of-type(1) > a'),
                'sign_in_button': (By.CSS_SELECTOR, '#secondary-navigation > ul.nav > li.ember-view.dropdown.sign-in > a.btn.btn-info.btn-top-login'),
            }
        }

        def verify(self):
            return self.current_service.text == 'PREPRINTS'
