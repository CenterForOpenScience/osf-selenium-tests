import settings

from selenium.webdriver.common.by import By

from base.locators import Locator
from pages.base import GuidBasePage, OSFBasePage


class ProjectPage(GuidBasePage):
    identity = Locator(By.CSS_SELECTOR, '#overview > nav#projectSubnav')
    project_title = Locator(By.ID, 'nodeTitleEditable', settings.LONG_TIMEOUT)


class MyProjectsPage(OSFBasePage):
    url = settings.OSF_HOME + '/myprojects/'

    identity = Locator(By.CSS_SELECTOR, '.col-xs-8 > h3:nth-child(1)')
