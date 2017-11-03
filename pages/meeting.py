import settings

from pages.base import OSFBasePage, Navbar
from selenium.webdriver.common.by import By

from utils  import purifyId


class MeetingPage(OSFBasePage):
    url = settings.OSF_HOME + '/meetings'

    locators = {
        **purifyId(OSFBasePage.locators),
        **{
            'identity': (By.CSS_SELECTOR, 'div.osf-meeting-header-img', settings.LONG_TIMEOUT),
            'register_button': (By.CSS_SELECTOR, 'div.osf-meeting-header-img div.osf-meeting-header div button[data-target="#osf-meeting-register"]', settings.LONG_TIMEOUT),
            'upload_button': (By.CSS_SELECTOR, 'div.osf-meeting-header-img div.osf-meeting-header div button[data-target="#osf-meeting-upload"]', settings.LONG_TIMEOUT),
        }
    }

    def __init__(self, driver, goto=True):
        super(MeetingPage, self).__init__(driver, goto)
        self.navbar = self.MeetingPageNavbar(driver)

    class MeetingPageNavbar(Navbar):

        locators = {
            **purifyId(Navbar.locators),
            **{
                'support_link': (By.XPATH, '/html/body/div[@class="osf-nav-wrapper]/nav[@id="navbarScope"]/div[@class="container"]/div[@id="secondary-navigation"]/ul/li[1]/a', settings.LONG_TIMEOUT),
                'donate_link': (By.XPATH, '/html/body/div[@class="osf-nav-wrapper]/nav[@id="navbarScope"]/div[@class="container"]/div[@id="secondary-navigation"]/ul/li[2]/a', settings.LONG_TIMEOUT),
            }
        }

        def verify(self):
            return self.current_service.text == 'MEETINGS'
