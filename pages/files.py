from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

import settings
from base.locators import (
    ComponentLocator,
    GroupLocator,
    Locator,
)
from components.navbars import RegistriesNavbar
from pages.base import (
    GuidBasePage,
    OSFBasePage,
)

class BaseFilesPage(OSFBasePage):

    # Components
    navbar = ComponentLocator(RegistriesNavbar)


class FilesListPage(BaseFilesPage):
    provider = 'osfstorage'
    guid = '4nrqw'
    url = settings.OSF_HOME + '/' + guid + '/' + 'files' + '/' + provider  + '/'

    # file name link
    file_link = Locator(By.CSS_SELECTOR, '[data-test-file-name]')

    # file actions menu trigger
    file_actions_menu = Locator(By.CSS_SELECTOR, '[data-test-file-download-share-trigger]')

    # download file
    download_file_action = Locator(By.CSS_SELECTOR, '[data-test-download-button]')

    # delete file
    delete_file_action = Locator(By.CSS_SELECTOR, '[]')

    # embed file
    embed_file_action = Locator(By.CSS_SELECTOR, '[data-test-embed-button]')

    # embed JS
    embed_js_action = Locator(By.CSS_SELECTOR, '[data-test-copy-js]')

    # embed HTML
    embed_html_action = Locator(By.CSS_SELECTOR, '[data-test-copy-htnml]')

    # share file
    share_file_action = Locator(By.CSS_SELECTOR, '[data-test-social-sharing-button]')

    # rename file
    rename_file_action = Locator(By.CSS_SELECTOR, '[]')

    # move file
    move_file_action = Locator(By.CSS_SELECTOR, '[]')
