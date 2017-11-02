import settings
from pages.base import OSFBasePage, Navbar
from selenium.webdriver.common.by import By


class RegistriesPage(OSFBasePage):
    url = settings.OSF_HOME + '/registries'

    locators = {
        **OSFBasePage.locators,
        **{
            'identity': (By.CSS_SELECTOR, 'body.ember-application > div.ember-view > div.preprints-page > div.search-header > div.container > div.row > div > div.registries-brand', settings.LONG_TIMEOUT),
        }
    }

    def __init__(self, driver, goto=True):
        super(RegistriesPage, self).__init__(driver, goto)
        self.navbar = self.RegistriesPageNavbar(driver)

    class RegistriesPageNavbar(Navbar):

        locators = {
            **Navbar.locators,
            **{
                'search_link': (By.XPATH, '/html/body/div[@class="ember-view]/div[1]/nav[@id="navbarScope"]/div[@class="container"]/div[@id="secondary-navigation"]/ul/li[1]/a'),
                'support_link': (By.XPATH, '/html/body/div[@class="ember-view]/div[1]/nav[@id="navbarScope"]/div[@class="container"]/div[@id="secondary-navigation"]/ul/li[2]/a'),
                'donate_link': (By.XPATH, '/html/body/div[@class="ember-view]/div[1]/nav[@id="navbarScope"]/div[@class="container"]/div[@id="secondary-navigation"]/ul/li[3]/a'),
                'user_dropdown': (By.CSS_SELECTOR, '#secondary-navigation > ul > li:nth-last-of-type(1) > a'),
                'sign_in_button': (By.LINK_TEXT, 'Sign in'),
            }
        }

        def verify(self):
            return self.current_service.text == 'REGISTRIES'
