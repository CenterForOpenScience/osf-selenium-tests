import pytest
import ipdb
#import markers
#import settings
from api import osf_api
from pages.project import FilesPage
#from pages.login import LoginPage, login, logout
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

def click_addon_row(files_page, target_file):
    row = find_addon_row(files_page, target_file)
    assert row is not None
    row.find_element_by_xpath('../..').click()
    return;

def find_addon_row(files_page, target_file):
    files_page.goto()
    files_page.first_file.present()  # checks files have loaded
    #return files_page
    found_it = False
    for row in files_page.fangorn_rows:
        if row.text == target_file:
            return row
    return;

def click_button(driver, button_name):
    file_action_buttons = driver.find_elements_by_css_selector('#folderRow .fangorn-toolbar-icon')
    for button in file_action_buttons:
        if button.text == button_name:
            button.click()
            break
    return;


@pytest.mark.usefixtures('must_be_logged_in')
class TestFilesPage:

    @pytest.mark.parametrize('provider', ['box'])
    def test_rename_file(self, driver, default_project, session, provider):
        node_id = default_project.id

        # connect addon to node, upload a single test file
        node = osf_api.get_node(session, node_id=node_id)
        if provider != 'osfstorage':
            addon = osf_api.get_user_addon(session, provider)
            addon_account_id = list(addon['data']['links']['accounts'])[0]
            osf_api.connect_provider_root_to_node(session, provider, addon_account_id,
                                                  node_id=node_id)
        new_file, metadata = osf_api.upload_fake_file(session=session, node=node, name='foo.txt',
                                                      provider=provider)

        files_page = FilesPage(driver, guid=node_id)

        click_addon_row(files_page, new_file)

        click_button(driver, 'Rename')
        rename_text_box = driver.find_element_by_id('renameInput')
        rename_text_box.clear()
        rename_text_box.send_keys('Selenium Test File')
        rename_text_box.send_keys(Keys.RETURN)

        # Wait for the first file in the add_on to be loaded
        files_page.first_file.present()

        row = find_addon_row(files_page, "foo.txtSelenium Test File")
        assert row is not None
        osf_api.delete_file(session, metadata['data']['links']['delete'])

    def test_checkout_file(self, driver, default_project, session):
        node_id = default_project.id
        provider = 'osfstorage'

        # connect addon to node, upload a single test file
        node = osf_api.get_node(session, node_id=node_id)
        new_file, metadata = osf_api.upload_fake_file(session=session, node=node, name='checkout.txt',
                                                      provider=provider)
        files_page = FilesPage(driver, guid=node_id)
        click_addon_row(files_page, new_file)

        click_button(driver, 'Check out file')
        driver.find_element_by_css_selector('.btn-warning').click()
        click_addon_row(files_page, 'checkout.txt')
        click_button(driver, 'Check in file')

        osf_api.delete_file(session, metadata['data']['links']['delete'])

    @pytest.mark.parametrize('provider', ['box'])
    def test_delete_file(self, driver, default_project, session, provider):
        node_id = default_project.id

        # connect addon to node, upload a single test file
        node = osf_api.get_node(session, node_id=node_id)
        if provider != 'osfstorage':
            addon = osf_api.get_user_addon(session, provider)
            addon_account_id = list(addon['data']['links']['accounts'])[0]
            osf_api.connect_provider_root_to_node(session, provider, addon_account_id,
                                                  node_id=node_id)

        new_file, metadata = osf_api.upload_fake_file(session=session, node=node, name='delete_this_guy.txt',
                                                      provider=provider)

        files_page = FilesPage(driver, guid=node_id)

        click_addon_row(files_page, new_file)
        click_button(driver, 'Delete')

        #wait for the delete confirmation
        files_page.delete_modal.present()

        # Front End will show 'delete failed' message - still works as expected
        driver.find_element_by_css_selector('.btn-danger').click()

        row = find_addon_row(files_page, 'delete_this_guy.txt')
        assert row is None

    @pytest.mark.parametrize('provider', ['box'])
    def test_dragon_drop(self, driver, default_project, session, provider):
        node_id = default_project.id

        # connect addon to node, upload a single test file
        node = osf_api.get_node(session, node_id=node_id)
        if provider != 'osfstorage':
            addon = osf_api.get_user_addon(session, provider)
            addon_account_id = list(addon['data']['links']['accounts'])[0]
            osf_api.connect_provider_root_to_node(session, provider, addon_account_id,
                                                      node_id=node_id)

        new_file, metadata = osf_api.upload_fake_file(session=session, node=node, name='drag_this_file.txt',
                                                          provider=provider)

        files_page = FilesPage(driver, guid=node_id)
        files_page.goto()
        files_page.first_file.present()  # checks files have loaded

        source = driver.find_element_by_css_selector('div.tb-row:nth-child(3)')
        target = driver.find_element_by_css_selector('div.tb-row:nth-child(4)')
        action_chains = ActionChains(driver)
        action_chains.drag_and_drop(source, target).perform()

        # Wait until the file is present
        files_page.first_file.present()


        '''
        Next steps:
        - Downloads? if there's a way
        - Writeable addons that WORK 'box', 'dropbox', 's3' , 'owncloud', 'figshare'
        -'googledrive' MUST specify both folder_id and folder_path
        -'github' Requested addon not currently configurable via API
        -'dataverse' Requested addon not currently configurable via API

        '''