import settings
import urllib.parse

from selenium.webdriver.common.by import By
from pages.base import OSFBasePage, Locator


class ProjectPage(OSFBasePage):

    # Locators
    identity = Locator(By.CSS_SELECTOR, '#overview > nav#projectSubnav')
    project_title = Locator(By.ID, 'nodeTitleEditable')

    def __init__(self, driver, verify=False, guid=None):
        super(self.__class__, self).__init__(driver, verify)
        self.url = urllib.parse.urljoin(settings.OSF_HOME, guid) if guid else None
