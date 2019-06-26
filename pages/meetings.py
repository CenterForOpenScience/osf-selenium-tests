import settings

from selenium.webdriver.common.by import By

from base.locators import Locator, ComponentLocator
from pages.base import OSFBasePage
from components.navbars import MeetingsNavbar


class BaseMeetingsPage(OSFBasePage):

    navbar = ComponentLocator(MeetingsNavbar)


class MeetingsPage(BaseMeetingsPage):
    url = settings.OSF_HOME + '/meetings/'

    identity = Locator(By.CSS_SELECTOR, 'img[alt="Logo for OSF meeting"]', settings.LONG_TIMEOUT)
    register_button = Locator(By.CSS_SELECTOR, 'button[data-test-register-button]', settings.LONG_TIMEOUT)
    register_text = Locator(By.CSS_SELECTOR, 'div[data-test-register-panel-text]')
    upload_button = Locator(By.CSS_SELECTOR, 'button[data-test-upload-button]', settings.LONG_TIMEOUT)
    upload_text = Locator(By.CSS_SELECTOR, 'div[data-test-upload-panel-text]')
    bottom_meeting_link = Locator(By.CSS_SELECTOR, '[data-test-meetings-list-list] li:last-of-type')
    filter_input = Locator(By.CSS_SELECTOR, 'input[class="ember-text-field ember-view"]')
    sort_caret_name_desc = Locator(By.CSS_SELECTOR, 'button[title="Sort descending"]')
    aps_logo = Locator(By.CSS_SELECTOR, ' img[data-test-aps-img]')
    bitss_logo = Locator(By.CSS_SELECTOR, 'img[data-test-bitss-img]')
    nrao_logo = Locator(By.CSS_SELECTOR, 'img[data-test-nrao-img]')
    spsp_logo = Locator(By.CSS_SELECTOR, 'img[data-test-spsp-img]')


class MeetingDetailPage(BaseMeetingsPage):
    url = settings.OSF_HOME + '/view/'

    identity = Locator(By.CSS_SELECTOR, '#grid > div > div > div.tb-head > div > input')
    meeting_title = Locator(By.CSS_SELECTOR, 'body > div.watermarked > div > h2')
    entry_download_button = Locator(By.CSS_SELECTOR, '#tb-tbody > div > div > div:nth-child(1) > div.tb-td.tb-col-4 > a > button > i')
    second_entry_link = Locator(By.CSS_SELECTOR, '#tb-tbody > div > div > div:nth-child(2) > div.tb-td.tb-col-0 > a')
    title = Locator(By.CSS_SELECTOR, '#nodeTitleEditable', settings.LONG_TIMEOUT)
    filter_input = Locator(By.CSS_SELECTOR, '#grid > div > div > div.tb-head > div > input')
    sort_caret_title_asc = Locator(By.CSS_SELECTOR, '#grid > div > div > div.tb-row-titles > div:nth-child(1) > i.fa.fa-chevron-up.tb-sort-inactive.asc-btn.m-r-xs')
