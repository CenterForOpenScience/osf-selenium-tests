import settings

from selenium.webdriver.common.by import By

from base.locators import Locator, ComponentLocator
from pages.base import OSFBasePage
from components.navbars import MeetingsNavbar


class BaseMeetingsPage(OSFBasePage):

    navbar = ComponentLocator(MeetingsNavbar)


class MeetingsPage(BaseMeetingsPage):
    url = settings.OSF_HOME + '/meetings/'

    identity = Locator(By.CSS_SELECTOR, 'div.osf-meeting-header-img', settings.LONG_TIMEOUT)
    register_button = Locator(By.CSS_SELECTOR, 'div.osf-meeting-header-img div.osf-meeting-header div button[data-target="#osf-meeting-register"]', settings.LONG_TIMEOUT)
    register_text = Locator(By.CSS_SELECTOR, '#osf-meeting-register > div:nth-child(1) > p:nth-child(1)')
    upload_button = Locator(By.CSS_SELECTOR, 'div.osf-meeting-header-img div.osf-meeting-header div button[data-target="#osf-meeting-upload"]', settings.LONG_TIMEOUT)
    upload_text = Locator(By.CSS_SELECTOR, '#osf-meeting-upload > div > ul > li:nth-child(2)')
    top_meeting_link = Locator(By.CSS_SELECTOR, '#tb-tbody > div > div > div:nth-child(1) > div.tb-td.tb-col-0 > a')
    filter_input = Locator(By.CSS_SELECTOR, '#meetings-grid > div > div > div.tb-head > div > input')
    sort_caret_name_desc = Locator(By.CSS_SELECTOR, '#meetings-grid > div > div > div.tb-row-titles > div:nth-child(1) > i.fa.fa-chevron-down.tb-sort-inactive.desc-btn')
    aps_logo = Locator(By.CSS_SELECTOR, 'body > div.watermarked > div.container.grey-background > div.row.org-logo.m-b-lg > div:nth-child(1) > a > img')
    bitss_logo = Locator(By.CSS_SELECTOR, 'body > div.watermarked > div.container.grey-background > div.row.org-logo.m-b-lg > div:nth-child(2) > a > img')
    nrao_logo = Locator(By.CSS_SELECTOR, 'body > div.watermarked > div.container.grey-background > div.row.org-logo.m-b-lg > div:nth-child(3) > a > img')
    spsp_logo = Locator(By.CSS_SELECTOR, 'body > div.watermarked > div.container.grey-background > div.row.org-logo.m-b-lg > div:nth-child(4) > a > img')


class MeetingDetailPage(BaseMeetingsPage):
    url = settings.OSF_HOME + '/view/'

    identity = Locator(By.CSS_SELECTOR, '#grid > div > div > div.tb-head > div > input')
    meeting_title = Locator(By.CSS_SELECTOR, 'body > div.watermarked > div > h2')
    entry_download_button = Locator(By.CSS_SELECTOR, '#tb-tbody > div > div > div:nth-child(1) > div.tb-td.tb-col-4 > a > button > i')
    second_entry_link = Locator(By.CSS_SELECTOR, '#tb-tbody > div > div > div:nth-child(2) > div.tb-td.tb-col-0 > a')
    project_title = Locator(By.CSS_SELECTOR, '#nodeTitleEditable', settings.LONG_TIMEOUT)
    filter_input = Locator(By.CSS_SELECTOR, '#grid > div > div > div.tb-head > div > input')
    sort_caret_title_asc = Locator(By.CSS_SELECTOR, '#grid > div > div > div.tb-row-titles > div:nth-child(1) > i.fa.fa-chevron-up.tb-sort-inactive.asc-btn.m-r-xs')
