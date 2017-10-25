import settings
import urllib.parse
from pages.base import OSFBasePage
from selenium.webdriver.common.by import By


class ProjectPage(OSFBasePage):

    locator_dictionary = {
        'project_title':(By.ID, 'nodeTitleEditable'),
    }

    def __init__(self, driver, guid=''):
        super(self.__class__, self).__init__(driver)
        self.url = urllib.parse.urljoin(settings.OSF_HOME, guid)
