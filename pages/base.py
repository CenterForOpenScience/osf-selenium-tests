import settings
from pages.base_components import BaseElement, Navbar

class BasePage(BaseElement):
    url = None

    def navigate(self):
        self.driver.get(self.url)

class OSFBasePage(BasePage):
    url = settings.DOMAIN
    navbar = Navbar()

    def is_logged_in(self):
        return self.navbar.logged_in()
