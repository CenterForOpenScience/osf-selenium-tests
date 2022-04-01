from selenium.webdriver.common.by import By

import settings
from base.locators import Locator
from pages.base import OSFBasePage


# Temporary Old Support Page - Delete this after eop: 0.139.0 preprints release
class OldSupportPage(OSFBasePage):
    url = settings.OSF_HOME + '/support'

    identity = Locator(By.CSS_SELECTOR, '._Support_15i3vw', settings.LONG_TIMEOUT)


class SupportPage(OSFBasePage):
    url = 'https://help.osf.io/'

    identity = Locator(By.CSS_SELECTOR, 'img[alt="OSF Support"]', settings.LONG_TIMEOUT)
