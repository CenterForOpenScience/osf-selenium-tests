import settings
import urllib.parse

from pages.base import OSFBasePage
from selenium.webdriver.common.by import By


class ProjectPage(OSFBasePage):

    locators = {
        'identity': (By.CSS_SELECTOR, '#overview > nav#projectSubnav'),
        'project_title': (By.ID, 'nodeTitleEditable'),
    }

    def __init__(self, driver, verify=False, guid=''):
        super(self.__class__, self).__init__(driver, verify)
        self.url = urllib.parse.urljoin(settings.OSF_HOME, guid)
