import pytest
import ipdb
import time
#import markers
#import settings
import requests

from api import osf_api
from pages.project import FilesPage
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver


def find_addon_row(files_page, target_file):
    files_page.goto()
    start_time = time.time()
    files_page.first_file.present()  # checks files have loaded
    file_present_time = time.time()

    #return files_page
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

def create_dictionary(files_page, driver):

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tb-tbody div[data-level="3"]')))
    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '#tb-tbody .fa-refresh')))

    all_fangorn_rows = driver.find_elements_by_css_selector('#treeGrid .tb-table .tb-tbody-inner > div > div')

    fangorn_dictionary = {}
    key = ""

    for row in all_fangorn_rows:
        data_level = row.get_attribute('data-level')
        print('\ndata-level = {}: text = {}'.format(data_level, row.text))
        if data_level == '2':
            key = row.text
            fangorn_dictionary[key] = []
        elif data_level == '3':
            fangorn_dictionary[key].append(row.text)

    print(fangorn_dictionary)



def format_provider_name(row):
    if row.text.startswith('Box:'):
        provider = 'box'
    elif row.text.startswith('Dropbox:'):
        provider = 'dropbox'
    elif row.text.startswith('Amazon S3:'):
        provider = 's3'
    elif row.text.startswith('ownCloud'):
        provider = 'owncloud'
    else:
        provider='provider name not found :('
    return provider;

@pytest.mark.usefixtures('must_be_logged_in')
class TestFilesPage:

    @pytest.mark.parametrize('provider', ['box', 'dropbox'])
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

        for _ in range(len(new_file)):
            rename_text_box.send_keys(Keys.BACKSPACE)

        rename_text_box.send_keys('Selenium Test File')
        rename_text_box.send_keys(Keys.RETURN)

        #TODO: Write another project.py->FilesPage->Locator to wait for renamed file
        time.sleep(5)

        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'tb-notify alert-success')))
        # WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'tb-notify alert-success')))

        row = find_addon_row(files_page, "Selenium Test File")
        assert row is not None

        osf_api.delete_file(session, metadata['data']['links']['delete'].replace('foo.txt', 'Selenium Test File'))


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

        #wait for the confirmation modal
        files_page.checkout_modal.present()

        driver.find_element_by_css_selector('.btn-warning').click()
        click_addon_row(files_page, 'checkout.txt')
        click_button(driver, 'Check in file')

        osf_api.delete_file(session, metadata['data']['links']['delete'])

    @pytest.mark.parametrize('provider', ['box', 'dropbox', 's3', 'owncloud'])
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

        #Negative Test Case
        row = find_addon_row(files_page, 'delete_this_guy.txt')
        assert row is None

    @pytest.mark.parametrize('provider, modifier_key, action', [
        ['box', 'none', 'move'],
        ['box', 'alt', 'copy'],
        ['dropbox', 'none', 'move'],
        ['dropbox', 'alt', 'copy'],
        ['owncloud', 'none', 'move'],
        ['owncloud', 'alt', 'copy'],
        ['s3', 'none', 'move'],
        ['s3', 'alt', 'copy']
    ])
    def test_dragon_drop(self, driver, default_project, session, provider, modifier_key, action):
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

        # checks files have loaded
        files_page.first_file.present()

        # Find the row that contains the new file
        for row in files_page.fangorn_rows:
            if row.text == 'drag_this_file.txt':
                source = row
                break;

        # Find the row with the OSF storage
        for row in files_page.fangorn_addons:
            if row.text=='OSF Storage (United States)':
                target = row
                break;

        action_chains = ActionChains(driver)

        if modifier_key=='alt':
            action_chains = ActionChains(driver)
            action_chains.key_down(Keys.LEFT_ALT)
            action_chains.click_and_hold(source)
            action_chains.move_to_element(target)
            action_chains.release()
            action_chains.key_up(Keys.LEFT_ALT)
            action_chains.perform()
        else:
            action_chains.drag_and_drop(source, target).perform()

        #TODO Change this to an implicit wait (polling)
        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'text-muted')))
        time.sleep(5)

        files_page.goto()
        row = find_addon_row('drag_this_file.txt')

        # Attempt to delete drag_this_file.txt in origin provider folder
        try:
            osf_api.delete_file(session, metadata['data']['links']['delete'])
        except:
            print("No file to be deleted")

    @pytest.mark.parametrize('provider', ['box', 'dropbox', 's3', 'owncloud'])
    def test_download_file(self, driver, default_project, session, provider):
        node_id = default_project.id

        # connect addon to node, upload a single test file
        node = osf_api.get_node(session, node_id=node_id)
        if provider != 'osfstorage':
            addon = osf_api.get_user_addon(session, provider)
            addon_account_id = list(addon['data']['links']['accounts'])[0]
            osf_api.connect_provider_root_to_node(session, provider, addon_account_id,
                                                  node_id=node_id)

        new_file, metadata = osf_api.upload_fake_file(session=session, node=node, name='download_file.txt',
                                                      provider=provider)

        files_page = FilesPage(driver, guid=node_id)
        files_page.goto()

        create_dictionary(files_page, driver)

        # click_addon_row(files_page, new_file)
        # click_button(driver, 'Download')
        # time.sleep(7)

        assert 'Could not retrieve file or directory' not in driver.find_element_by_xpath('/html/body').text

        osf_api.delete_file(session, metadata['data']['links']['delete'])

        # assert response.status_code == '200'


        '''
        Next steps:
        - dragon_drop needs an implicit wait
            - Ask Fitz
            
        - Downloads
            - Click downloads button
            - Check for a 200 status  
            
        - Dictionary
            - # create_dictionary(files_page)
            - change n -> 1 in the next line
            - row = driver.find_element_by_css_selector('#tb-tbody > div > div > div:nth-child(n)')
            - val = row.get_attribute('data-level')
            - clean up provider & filenames
            - update and return dictionary from function
            
        - EC Waits
            - Explain the purpose & reasoning for the new waits
            
        Josh Testing Notes
        Drag and Drop
        - Target add-on needs to be visible in the files widget
        
        Delete btn-danger 
        - Modal must be in current window for test to pass
        - User cannot be in a separate window while test is running
            
        Writeable addons (that work)
        - 'box', 'dropbox', 's3', 'owncloud'
        
        'googledrive' - MUST specify both folder_id and folder_path
        'github' - requested add-on not currently configurable via API
        'dataverse' - requested add-on not currently configurable via API
        'figshare' - has a weird file setup
        
        '''