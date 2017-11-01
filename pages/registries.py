import settings
from pages.base import OSFBasePage, Navbar
from selenium.webdriver.common.by import By


class RegistriesPage(OSFBasePage):
    url = settings.OSF_HOME + '/registries'

    def __init__(self, driver, goto=True):
        super(RegistriesPage, self).__init__(driver, goto)
        self.navbar = self.RegistriesPageNavbar(driver)

    def verify(self):
        return len(self.driver.find_elements(By.CSS_SELECTOR, 'div.registries-brand')) == 1

    class RegistriesPageNavbar(Navbar):

        def verify(self):
            return self.current_service.text == 'REGISTRIES'
