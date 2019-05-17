import pytest
import ipdb
import time
#import markers
#import settings
from api import osf_api
from pages.project import FilesPage
#from pages.login import LoginPage, login, logout
from selenium.webdriver.common.keys import Keys

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
        files_page.goto()
        files_page.first_file.present()  # checks files have loaded
        found_it = False
        for row in files_page.fangorn_rows:
            if row.text == new_file:
                found_it = True
                row.find_element_by_xpath('../..').click()  # get grandparent
                break
        assert found_it

        file_action_buttons = driver.find_elements_by_css_selector('#folderRow .fangorn-toolbar-icon')
        for button in file_action_buttons:
            if button.text == 'Rename':
                button.click()
                rename_text_box = driver.find_element_by_id('renameInput')
                rename_text_box.clear()
                rename_text_box.send_keys('Selenium Test File')
                rename_text_box.send_keys(Keys.RETURN)
                time.sleep(5)
                break

        files_page.goto()
        files_page.first_file.present()  # checks files have loaded
        found_it = False
        for row in files_page.fangorn_rows:
            if row.text == "foo.txtSelenium Test File":
                found_it = True
                #row.find_element_by_xpath('../..').click()  # get grandparent
                break
        assert found_it

        osf_api.delete_file(session, metadata['data']['links']['delete'])

    def test_checkout_file(self, driver, default_project, session):
        node_id = default_project.id
        provider = 'osfstorage'

        # connect addon to node, upload a single test file
        node = osf_api.get_node(session, node_id=node_id)
        new_file, metadata = osf_api.upload_fake_file(session=session, node=node, name='checkout.txt',
                                                      provider=provider)

        files_page = FilesPage(driver, guid=node_id)
        files_page.goto()
        files_page.first_file.present()  # checks files have loaded
        found_it = False
        for row in files_page.fangorn_rows:
            if row.text == new_file:
                found_it = True
                row.find_element_by_xpath('../..').click()  # get grandparent
                break
        assert found_it

        file_action_buttons = driver.find_elements_by_css_selector('#folderRow .fangorn-toolbar-icon')
        for button in file_action_buttons:
            if button.text == 'Check out file':
                button.click()
                break

        driver.find_element_by_css_selector('.btn-warning').click()
        found_it = False

        files_page.first_file.present()
        for row in files_page.fangorn_rows:
            if row.text == 'checkout.txt':
                found_it = True
                row.find_element_by_xpath('../..').click()  # get grandparent
                break
        assert found_it

        found_it = False
        file_action_buttons = driver.find_elements_by_css_selector('#folderRow .fangorn-toolbar-icon')
        for button in file_action_buttons:
            if button.text == 'Check in file':
                found_it = True
                button.click()
        assert found_it

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
        # wrap in a try/catch
        # webdriver exception = load the file
        new_file, metadata = osf_api.upload_fake_file(session=session, node=node, name='delete_this_guy.txt',
                                                      provider=provider)

        files_page = FilesPage(driver, guid=node_id)
        files_page.goto()
        files_page.first_file.present()  # checks files have loaded
        found_it = False
        for row in files_page.fangorn_rows:
            if row.text == new_file:
                found_it = True
                row.find_element_by_xpath('../..').click()  # get grandparent
                break
        assert found_it


        file_action_buttons = driver.find_elements_by_css_selector('#folderRow .fangorn-toolbar-icon')
        for button in file_action_buttons:
            if button.text == 'Delete':
                button.click()
                break

        driver.find_element_by_css_selector('.btn-danger').click()

        files_page.first_file.present()

        found_it = False
        for row in files_page.fangorn_rows:
            if row.text == 'delete_this_guy.txt':
                found_it = True
                row.find_element_by_xpath('../..').click()  # get grandparent
                break
        assert not found_it

        '''
        Next steps:
        - Checkouts
        - Downloads? if there's a way
        - Writeable addons that WORK 'box', 'dropbox', 's3' , 'owncloud', 'figshare'
        -'googledrive' MUST specify both folder_id and folder_path
        -'github' Requested addon not currently configurable via API
        -'dataverse' Requested addon not currently configurable via API

        '''