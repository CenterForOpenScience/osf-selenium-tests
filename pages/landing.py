import settings

from selenium.webdriver.common.by import By

from pages.base import OSFBasePage
from components.navbars import EmberNavbar
from base.locators import Locator, ComponentLocator


class EmberLandingPage(OSFBasePage):
    identity = Locator(By.ID, 'home-hero', settings.LONG_TIMEOUT)

    # Components
    navbar = ComponentLocator(EmberNavbar)


class LandingPage(OSFBasePage):
    waffle_override = {'ember_home_page': EmberLandingPage}

    identity = Locator(By.ID, 'home-hero', settings.LONG_TIMEOUT)
