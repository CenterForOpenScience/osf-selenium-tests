import settings

from selenium.webdriver.common.by import By
from pages.base import OSFBasePage, Navbar, Locator

class MeetingPage(OSFBasePage):
    url = settings.OSF_HOME + '/meetings'

    # Locators
    identity = Locator(By.CSS_SELECTOR, 'div.osf-meeting-header-img', settings.LONG_TIMEOUT)
    register_button = Locator(By.CSS_SELECTOR, 'div.osf-meeting-header-img div.osf-meeting-header div button[data-target="#osf-meeting-register"]', settings.LONG_TIMEOUT)
    upload_button = Locator(By.CSS_SELECTOR, 'div.osf-meeting-header-img div.osf-meeting-header div button[data-target="#osf-meeting-upload"]', settings.LONG_TIMEOUT)

    def __init__(self, driver, verify=False):
        super(MeetingPage, self).__init__(driver, verify)
        self.navbar = self.MeetingPageNavbar(driver)

    class MeetingPageNavbar(Navbar):

        # Locators
        support_link = Locator(By.LINK_TEXT, 'Support')

        def verify(self):
            return self.current_service.text == 'MEETINGS'
