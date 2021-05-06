import settings

from api import osf_api
from selenium.webdriver.common.by import By

from components.navbars import EmberNavbar
from pages.base import OSFBasePage, GuidBasePage
from base.locators import Locator, ComponentLocator, GroupLocator


class BaseQuickfilesPage(OSFBasePage):

    navbar = ComponentLocator(EmberNavbar)


class QuickfilesPage(BaseQuickfilesPage, GuidBasePage):
    """Main page for a user's quickfiles. Take's a user's guid, but defaults to USER_ONE's if a guid isn't given.
    """
    base_url = settings.OSF_HOME + '/{guid}/quickfiles/'
    user = osf_api.current_user()

    def __init__(self, driver, verify=False, guid=user.id):
        super().__init__(driver, verify, guid)

    # TODO: Add download buttons back in when you have a way to distingish them
    identity = Locator(By.CSS_SELECTOR, '#quickfiles-dropzone')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale')
    upload_button = Locator(By.CSS_SELECTOR, '.dz-upload-button')
    share_button = Locator(By.CSS_SELECTOR, '.btn .fa-share-alt')
    view_button = Locator(By.CSS_SELECTOR, '[data-test-view-button]')
    help_button = Locator(By.CSS_SELECTOR, '.btn .fa-info')
    filter_button = Locator(By.CSS_SELECTOR, '.btn .fa-search')
    rename_button = Locator(By.CSS_SELECTOR, '[data-test-rename-file-button]')
    delete_button = Locator(By.CSS_SELECTOR, '[data-test-delete-file-button]')
    move_button = Locator(By.CSS_SELECTOR, '[data-test-move-button]')

    # Group Locators
    files = GroupLocator(By.CSS_SELECTOR, '._file-browser-item_1v8xgw')
    file_titles = GroupLocator(By.CSS_SELECTOR, '._file-browser-item_1v8xgw a')


class QuickfileDetailPage(BaseQuickfilesPage, GuidBasePage):
    identity = Locator(By.CSS_SELECTOR, '._TitleBar_1628nl')
