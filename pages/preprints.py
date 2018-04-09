import settings

from selenium.webdriver.common.by import By

from base.locators import Locator, ComponentLocator
from components.navbars import PreprintsNavbar
from pages.base import OSFBasePage


class BasePreprintPage(OSFBasePage):
        navbar = ComponentLocator(PreprintsNavbar)


class PreprintPage(BasePreprintPage):
    url = settings.OSF_HOME + '/preprints/'

    identity = Locator(By.CSS_SELECTOR, 'body.ember-application > div.ember-view > div.preprints-page > div.preprint-header', settings.LONG_TIMEOUT)
    add_preprint_link = Locator(By.CSS_SELECTOR, 'div.preprint-page div.preprint-header div.container div div a[href="/preprints/submit"]', settings.LONG_TIMEOUT)


class SubmitPreprintPage(BasePreprintPage):
    url = settings.OSF_HOME + '/preprints/submit/'

    identity = Locator(By.CSS_SELECTOR, 'div.preprint-submit-header')
