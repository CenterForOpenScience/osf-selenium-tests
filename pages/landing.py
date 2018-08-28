import settings

from selenium.webdriver.common.by import By

from pages.base import OSFBasePage
from components.navbars import EmberNavbar
from base.locators import Locator, ComponentLocator


class LandingPage(OSFBasePage):
    identity = Locator(By.ID, 'home-hero', settings.LONG_TIMEOUT)

    # Components
    navbar = ComponentLocator(EmberNavbar)


class LegacyLandingPage(OSFBasePage):
    waffle_override = {'ember_home_page': LandingPage}

    identity = Locator(By.ID, 'home-hero', settings.LONG_TIMEOUT)
