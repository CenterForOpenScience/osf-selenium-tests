import settings

from selenium.webdriver.common.by import By

from base.locators import Locator, ComponentLocator
from pages.base import OSFBasePage
from components.navbars import EmberNavbar

class InstitutionsLandingPage(OSFBasePage):
    url = settings.OSF_HOME + '/institutions/'

    identity = Locator(By.CSS_SELECTOR, '._Institutions__header-logo_1ycvu9')

    #TODO: add institutional navbar
    navbar = ComponentLocator(EmberNavbar)

class InstitutionBrandedPage(OSFBasePage):

    identity = Locator(By.CSS_SELECTOR, '#fileBrowser > div.db-header.row > div.db-buttonRow.col-xs-12.col-sm-4.col-lg-3 > div > input')
