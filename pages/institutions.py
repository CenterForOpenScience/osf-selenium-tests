import settings

from selenium.webdriver.common.by import By

from base.locators import Locator, ComponentLocator, GroupLocator
from pages.base import OSFBasePage
from components.navbars import EmberNavbar

class InstitutionsLandingPage(OSFBasePage):
    url = settings.OSF_HOME + '/institutions/'

    identity = Locator(By.CSS_SELECTOR, '._Institutions__header-logo_1ycvu9')

    search_bar = Locator(By.CSS_SELECTOR, '.ember-text-field')

    # Group Locators
    institution_list = GroupLocator(By.CSS_SELECTOR, '._Institutions__table__item_1ycvu9 span')

    #TODO: add institutional navbar
    navbar = ComponentLocator(EmberNavbar)

class InstitutionBrandedPage(OSFBasePage):

    identity = Locator(By.CSS_SELECTOR, '#fileBrowser > div.db-header.row > div.db-buttonRow.col-xs-12.col-sm-4.col-lg-3 > div > input')
