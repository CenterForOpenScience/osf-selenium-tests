import urllib.parse
from pages.base import OSFBasePage
from selenium.webdriver.common.by import By

class ProjectPage(OSFBasePage):
    title_loc = (By.ID, 'nodeTitleEditable')

    # It's optional to pass a project pages a guid.
    def __init__(self, guid=''):
        super(ProjectPage, self).__init__()
        self.url = urllib.parse.urljoin(self.url, guid)

    def get_title(self):
        return self._find_element(*self.title_loc).text
