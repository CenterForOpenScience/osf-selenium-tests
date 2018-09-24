import settings

from selenium.webdriver.common.by import By

from base.locators import Locator, ComponentLocator
from components.navbars import RegistriesNavbar
from pages.base import OSFBasePage


class RegistriesPage(OSFBasePage):
    url = settings.OSF_HOME + '/registries'

    identity = Locator(By.CSS_SELECTOR, '._RegistriesHeader_3zbd8x', settings.LONG_TIMEOUT)

    # Components
    navbar = ComponentLocator(RegistriesNavbar)
