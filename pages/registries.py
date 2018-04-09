import settings

from selenium.webdriver.common.by import By

from base.locators import Locator, ComponentLocator
from components.navbars import RegistriesNavbar
from pages.base import OSFBasePage


class RegistriesPage(OSFBasePage):
    url = settings.OSF_HOME + '/registries'

    identity = Locator(By.CSS_SELECTOR, 'body.ember-application > div.ember-view > div.preprints-page > div.search-header > div.container > div.row > div > div.registries-brand', settings.LONG_TIMEOUT)

    # Components
    navbar = ComponentLocator(RegistriesNavbar)
