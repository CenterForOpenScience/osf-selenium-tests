import settings

from pages.base import OSFBasePage, Navbar
from selenium.webdriver.common.by import By


class MeetingPage(OSFBasePage):
    url = settings.OSF_HOME + '/meetings'

    locators = {
        'identity': (By.CSS_SELECTOR, 'div.osf-meeting-header-img', settings.LONG_TIMEOUT),
        'register_button': (By.CSS_SELECTOR, 'div.osf-meeting-header-img div.osf-meeting-header div button[data-target="#osf-meeting-register"]', settings.LONG_TIMEOUT),
        'upload_button': (By.CSS_SELECTOR, 'div.osf-meeting-header-img div.osf-meeting-header div button[data-target="#osf-meeting-upload"]', settings.LONG_TIMEOUT),
    }

    def __init__(self, driver, verify=False):
        super(MeetingPage, self).__init__(driver, verify)
        self.navbar = self.MeetingPageNavbar(driver)

    class MeetingPageNavbar(Navbar):

        def verify(self):
            return self.current_service.text == 'MEETINGS'
