import settings

from selenium.webdriver.common.by import By
from base.locators import Locator
from pages.base import OSFBasePage


class MyRegistrationsPage(OSFBasePage):
    url = settings.OSF_HOME + '/registries/my-registrations/'
    identity = Locator(By.CSS_SELECTOR, 'div[data-analytics-scope="My Registrations page"]')
