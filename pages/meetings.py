import settings

from selenium.webdriver.common.by import By

from base.locators import Locator, ComponentLocator
from pages.base import OSFBasePage
from components.navbars import MeetingsNavbar



class BaseMeetingsPage(OSFBasePage):

    def __init__(self, driver, verify=False):
        super(BaseMeetingsPage, self).__init__(driver, verify)
        self.navbar = self.MeetingsPageNavbar(driver)

    class MeetingsPageNavbar(Navbar):

        # Locators
        support_link = Locator(By.LINK_TEXT, 'Support')

        def verify(self):
            return self.current_service.text == 'MEETINGS'


class MeetingsPage(BaseMeetingsPage):
    url = settings.OSF_HOME + '/meetings'

    identity = Locator(By.CSS_SELECTOR, 'div.osf-meeting-header-img', settings.LONG_TIMEOUT)
    register_button = Locator(By.CSS_SELECTOR, 'div.osf-meeting-header-img div.osf-meeting-header div button[data-target="#osf-meeting-register"]', settings.LONG_TIMEOUT)
    register_text = Locator(By.CSS_SELECTOR, '#osf-meeting-register > div:nth-child(1) > p:nth-child(1)')
    upload_button = Locator(By.CSS_SELECTOR, 'div.osf-meeting-header-img div.osf-meeting-header div button[data-target="#osf-meeting-upload"]', settings.LONG_TIMEOUT)
    upload_text = Locator(By.CSS_SELECTOR, '#osf-meeting-upload > div > ul > li:nth-child(2)')
    top_meeting_link = Locator(By.CSS_SELECTOR, '#tb-tbody > div > div > div:nth-child(1) > div.tb-td.tb-col-0 > a')
    aps_logo = Locator(By.CSS_SELECTOR, 'body > div.watermarked > div.container.grey-background > div.row.org-logo.m-b-lg > div:nth-child(1) > a > img')
    bitss_logo = Locator(By.CSS_SELECTOR, 'body > div.watermarked > div.container.grey-background > div.row.org-logo.m-b-lg > div:nth-child(2) > a > img')
    nrao_logo = Locator(By.CSS_SELECTOR, 'body > div.watermarked > div.container.grey-background > div.row.org-logo.m-b-lg > div:nth-child(3) > a > img')
    spsp_logo = Locator(By.CSS_SELECTOR, 'body > div.watermarked > div.container.grey-background > div.row.org-logo.m-b-lg > div:nth-child(4) > a > img')

    # Components
    navbar = ComponentLocator(MeetingsNavbar)

class MeetingDetailPage(BaseMeetingsPage):
    url = settings.OSF_HOME + '/view/'

    # Locators
    identity = Locator(By.CSS_SELECTOR, '#grid > div > div > div.tb-head > div > input')
    meeting_title = Locator(By.CSS_SELECTOR, 'body > div.watermarked > div > h2')
