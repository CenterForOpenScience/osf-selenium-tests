import settings

from selenium.webdriver.common.by import By

from base.locators import Locator, ComponentLocator
from pages.base import OSFBasePage
from components.navbars import MeetingsNavbar


class MeetingsPage(OSFBasePage):
    url = settings.OSF_HOME + '/meetings'

    identity = Locator(By.CSS_SELECTOR, 'div.osf-meeting-header-img', settings.LONG_TIMEOUT)
    register_button = Locator(By.CSS_SELECTOR, 'div.osf-meeting-header-img div.osf-meeting-header div button[data-target="#osf-meeting-register"]', settings.LONG_TIMEOUT)
    register_text = Locator(By.CSS_SELECTOR, '#osf-meeting-register > div:nth-child(1) > p:nth-child(1)')
    upload_button = Locator(By.CSS_SELECTOR, 'div.osf-meeting-header-img div.osf-meeting-header div button[data-target="#osf-meeting-upload"]', settings.LONG_TIMEOUT)
    upload_text = Locator(By.CSS_SELECTOR, '#osf-meeting-upload > div > ul > li:nth-child(2)')
    top_meeting_link = Locator(By.CSS_SELECTOR, '#tb-tbody > div > div > div:nth-child(1) > div.tb-td.tb-col-0 > a')

    # Components
    navbar = ComponentLocator(MeetingsNavbar)
