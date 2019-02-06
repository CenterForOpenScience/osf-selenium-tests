import settings

from urllib.parse import urljoin
from selenium.webdriver.common.by import By

from base.locators import Locator, ComponentLocator, GroupLocator
from components.navbars import RegistriesNavbar
from pages.base import OSFBasePage, GuidBasePage


class BaseRegistriesPage(OSFBasePage):

    # Components
    navbar = ComponentLocator(RegistriesNavbar)

class RegistriesLandingPage(BaseRegistriesPage):
    url = settings.OSF_HOME + '/registries'

    identity = Locator(By.CSS_SELECTOR, '._RegistriesHeader_3zbd8x', settings.LONG_TIMEOUT)
    search_button = Locator(By.CSS_SELECTOR, '[data-test-search-button]')

class RegistriesDiscoverPage(BaseRegistriesPage):
    url = settings.OSF_HOME + '/registries/discover'

    identity = Locator(By.CSS_SELECTOR, '[data-test-share-logo]')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale')

    # Group Locators
    search_results = GroupLocator(By.CSS_SELECTOR, '._SearchResult_10ty34')

class RegistrationDetailPage(GuidBasePage):
    url_base = urljoin(settings.OSF_HOME, '{guid}')
    identity = Locator(By.CSS_SELECTOR, '[data-test-result-title-id]')
    title = Locator(By.CSS_SELECTOR, '[data-test-result-title-id]')
