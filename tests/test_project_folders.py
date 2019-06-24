import pytest
import ipdb
import time
# import markers
# import settings
from api import osf_api
from pages.project import FilesPage
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def find_addon_row(files_page, target_file):
    files_page.goto()
    start_time = time.time()
    files_page.first_file.present()  # checks files have loaded
    file_present_time = time.time()

    # return files_page
    for row in files_page.fangorn_rows:
        if row.text == target_file:
            end_time = time.time()
            elapsed_time = end_time - start_time
            found_time = file_present_time - start_time
            print("Elapsed Time: ", elapsed_time)
            print("Found Time: ", found_time)
            return row
    return;


def click_addon_row(files_page, target_file):
    row = find_addon_row(files_page, target_file)
    assert row is not None
    row.find_element_by_xpath('../..').click()
    return;


# Click a button in the toolbar, just pass in the name
def click_button(driver, button_name):
    file_action_buttons = driver.find_elements_by_css_selector('#folderRow .fangorn-toolbar-icon')
    for button in file_action_buttons:
        if button.text == button_name:
            button.click()
            break
    return;


def click_addon_folder(files_page, target_file):
    files_page.goto()
    time.sleep(4)

    for row in files_page.fangorn_folders:
        if row.find_element_by_xpath('../../..').text == target_file:
            row.click()
            break;
    return;

def format_provider_name(row):
    if row.text=='Box: / (Full Box)':
        provider = 'box'
    elif row.text=='Dropbox: / (Full Dropbox)':
        provider = 'dropbox'
    elif row.text=='Amazon S3: elasticbeanstalk-us-east-1-593772593292 (US Standard)':
        provider = 's3'
    elif row.text=='ownCloud: / (Full ownCloud)':
        provider = 'owncloud'
    else:
        provider='provider name not found :('
    return provider;


@pytest.mark.usefixtures('must_be_logged_in')
class TestFilesPage:

    @pytest.mark.parametrize('provider', ['box'])
    def test_delete_folder(self, driver, default_project, session, provider):
        node_id = default_project.id

        # connect addon to node, upload a single test file
        node = osf_api.get_node(session, node_id=node_id)
        if provider != 'osfstorage':
            addon = osf_api.get_user_addon(session, provider)
            addon_account_id = list(addon['data']['links']['accounts'])[0]
            osf_api.connect_provider_root_to_node(session, provider, addon_account_id,
                                                  node_id=node_id)

            new_folder, metadata = osf_api.upload_fake_folder(session=session, node=node, name='Selenium Test Folder',
                                                            provider=provider)

            files_page = FilesPage(driver, guid=node_id)
            files_page.goto()

            # checks files have loaded
            files_page.first_file.present()

            # do implicit wait
            time.sleep(4)
            click_addon_folder(files_page, new_folder)
            click_button(driver, 'Delete Folder')

            # wait for the delete confirmation
            files_page.delete_modal.present()

            # Front End will show 'delete failed' message - still works as expected
            driver.find_element_by_css_selector('.btn-danger').click()


    @pytest.mark.parametrize('provider', ['box'])
    def test_create_folder(self, driver, default_project, session, provider):
        node_id = default_project.id

        # connect addon to node, upload a single test file
        node = osf_api.get_node(session, node_id=node_id)
        if provider != 'osfstorage':
            addon = osf_api.get_user_addon(session, provider)
            addon_account_id = list(addon['data']['links']['accounts'])[0]
            osf_api.connect_provider_root_to_node(session, provider, addon_account_id,
                                                  node_id=node_id)

            files_page = FilesPage(driver, guid=node_id)
            files_page.goto()

            # checks files have loaded
            files_page.first_file.present()

            # Find the row with the OSF storage
            for row in files_page.fangorn_addons:
                if format_provider_name(row) == provider:
                    row.click()
                    break;

            click_button(driver, 'Create Folder')
            folder_name_text_box = driver.find_element_by_id('createFolderInput')
            folder_name_text_box.click()
            folder_name_text_box.send_keys('Selenium Test Folder')
            folder_name_text_box.send_keys(Keys.RETURN)

            # do implicit wait
            time.sleep(4)
            click_addon_folder(files_page, 'Selenium Test Folder')
            click_button(driver, 'Delete Folder')

            # wait for the delete confirmation
            files_page.delete_modal.present()

            # Front End will show 'delete failed' message - still works as expected
            driver.find_element_by_css_selector('.btn-danger').click()

    @pytest.mark.parametrize('provider', ['box'])
    def test_rename_folder(self, driver, default_project, session, provider):
        node_id = default_project.id

        # connect addon to node, upload a single test file
        node = osf_api.get_node(session, node_id=node_id)
        if provider != 'osfstorage':
            addon = osf_api.get_user_addon(session, provider)
            addon_account_id = list(addon['data']['links']['accounts'])[0]
            osf_api.connect_provider_root_to_node(session, provider, addon_account_id,
                                                  node_id=node_id)

            new_folder, metadata = osf_api.upload_fake_folder(session=session, node=node, name='Selenium Test Folder',
                                                            provider=provider)

            files_page = FilesPage(driver, guid=node_id)
            files_page.goto()

            # checks files have loaded
            files_page.first_file.present()

            # Rename
            time.sleep(4)
            click_addon_folder(files_page, 'Selenium Test Folder')
            click_button(driver, 'Rename')
            folder_name_text_box = driver.find_element_by_id('renameInput')
            folder_name_text_box.click()
            for _ in range(len(new_folder)):
                folder_name_text_box.send_keys(Keys.BACKSPACE)
            folder_name_text_box.send_keys('Automated Folder')
            folder_name_text_box.send_keys(Keys.RETURN)

            # do implicit wait
            time.sleep(4)
            click_addon_folder(files_page, 'Automated Folder')
            click_button(driver, 'Delete Folder')

            # wait for the delete confirmation
            files_page.delete_modal.present()

            # Front End will show 'delete failed' message - still works as expected
            driver.find_element_by_css_selector('.btn-danger').click()


        '''
        Next steps:
        Downloads
        - Click downloads button
        - Check for a 200 status 
        
        API
        - Write a delete call for Folders
           
        Folders for all addons
        - Move
        - Copy
        - Rename
        - Delete

        '''