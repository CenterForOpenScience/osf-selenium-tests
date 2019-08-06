import pytest
import time
# import ipdb
# import markers
# import settings

from api import osf_api
from pages.project import FilesPage
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

'''
*** Next steps ***
Update sleeps with implicit waits
    - Work w/Fitz
Downloads
    - Firefox - S3 still opens prompt
    - Click downloads button
    - Check for a 200 status
Drag and Drop
    - Doesn't work for Chrome
*** Josh Testing Notes ***
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


def format_provider_name(row):
    if row.text.startswith('Box:'):
        provider = 'box'
    elif row.text.startswith('Dropbox:'):
        provider = 'dropbox'
    elif row.text.startswith('Amazon S3:'):
        provider = 's3'
    elif row.text.startswith('ownCloud'):
        provider = 'owncloud'
    elif row.text.startswith('osfstorage'):
        provider = 'osf'
    elif row.text.startswith('OSF'):
        provider = 'osf'
    else:
        provider = 'provider name not found :('
    return provider

def create_dictionary(driver):
    # Wait until fangorn has loaded all files in the tree before testing
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tb-tbody div[data-level="3"]')))
    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '#tb-tbody .fa-refresh')))

    all_fangorn_rows = driver.find_elements_by_css_selector('#treeGrid .tb-table .tb-tbody-inner > div > div')
    fangorn_dictionary = {}
    key = ''

    for row in all_fangorn_rows:
        data_level = row.get_attribute('data-level')
        if data_level == '2':
            key = format_provider_name(row)
            fangorn_dictionary[key] = []
        elif data_level == '3':
            file_name = row.find_element_by_css_selector('.td-title .title-text')
            # create sub-dictionary entries for each provider
            # each sub-dictionary contains name of the row and the row object
            fangorn_dictionary[key].append({'file_name': file_name.text, 'row_object': row})

    return fangorn_dictionary

def find_row_by_name(driver, provider, row_name):
    all_files = create_dictionary(driver)
    for x in all_files[provider]:
        if x['file_name'] == row_name:
            return x['row_object']
    return

# Click a button in the toolbar, just pass in the name
def find_toolbar_button_by_name(driver, button_name):
    file_action_buttons = driver.find_elements_by_css_selector('#folderRow .fangorn-toolbar-icon')
    for button in file_action_buttons:
        if button.text == button_name:
            return button
    return

@pytest.mark.usefixtures('must_be_logged_in')
class TestFilesPage:

    @pytest.mark.parametrize('provider', ['owncloud'])
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

        row = find_row_by_name(driver, provider, new_file)
        row.click()
        rename_button = find_toolbar_button_by_name(driver, 'Rename')
        rename_button.click()
        rename_text_box = driver.find_element_by_id('renameInput')

        for _ in range(len(new_file)):
            rename_text_box.send_keys(Keys.BACKSPACE)

        new_name = 'Selenium Test File'
        rename_text_box.send_keys(new_name)
        rename_text_box.send_keys(Keys.RETURN)
        time.sleep(5)

        # test old file name does not exist
        old_file = find_row_by_name(driver, provider, 'foo.txt')
        assert old_file is None

        # test that new file name is present and visible
        renamed_file = find_row_by_name(driver, provider, 'Selenium Test File')
        assert 'Selenium Test File' in renamed_file.text

        osf_api.delete_file(session, metadata['data']['links']['delete'].replace('foo.txt', 'Selenium Test File'))

    def test_checkout_file(self, driver, default_project, session):
        node_id = default_project.id
        provider = 'osfstorage'

        # connect add-on to node, upload a single test file
        node = osf_api.get_node(session, node_id=node_id)
        new_file, metadata = osf_api.upload_fake_file(session=session, node=node, name='checkout.txt',
                                                      provider=provider)
        files_page = FilesPage(driver, guid=node_id)
        files_page.goto()

        row = find_row_by_name(driver, 'osf', new_file)
        row.click()
        checkout_button = find_toolbar_button_by_name(driver, 'Check out file')
        checkout_button.click()

        # Accept the confirmation modal
        driver.find_element_by_css_selector('.btn-warning').click()
        time.sleep(4)

        # Test that Check Out button is no longer present
        row = find_row_by_name(driver, 'osf', new_file)
        row.click()
        checkout_button = find_toolbar_button_by_name(driver, 'Check out file')
        assert checkout_button is None

        row = find_row_by_name(driver, 'osf', new_file)
        row.click()
        check_in_button = find_toolbar_button_by_name(driver, 'Check in file')
        check_in_button.click()
        time.sleep(4)

        # Test that Check In button is no longer present
        row = find_row_by_name(driver, 'osf', new_file)
        row.click()
        check_in_button = find_toolbar_button_by_name(driver, 'Check in file')
        assert check_in_button is None

        osf_api.delete_file(session, metadata['data']['links']['delete'])

    @pytest.mark.parametrize('provider', ['s3'])
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
        files_page.goto()

        row = find_row_by_name(driver, provider, new_file)
        row.click()
        delete_button = find_toolbar_button_by_name(driver, 'Delete')
        delete_button.click()

        # wait for the delete confirmation
        files_page.delete_modal.present()

        # Front End will show 'delete failed' message - still works as expected
        driver.find_element_by_css_selector('.btn-danger').click()
        time.sleep(4)

        deleted_row = find_row_by_name(driver, provider, new_file)
        assert deleted_row is None

    @pytest.mark.parametrize('provider, modifier_key, action', [
        ['box', 'none', 'move'],
        ['box', 'alt', 'copy']
        # ['dropbox', 'none', 'move'],
        # ['dropbox', 'alt', 'copy'],
        # ['owncloud', 'none', 'move'],
        # ['owncloud', 'alt', 'copy'],
        # ['s3', 'none', 'move'],
        # ['s3', 'alt', 'copy']
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

        # Find the row that contains the new file
        source = find_row_by_name(driver, provider, new_file)

        # Find the row with the OSF storage
        for row in files_page.fangorn_addons:
            if row.text == 'OSF Storage (United States)':
                target = row
                break

        action_chains = ActionChains(driver)
        if modifier_key == 'alt':
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

        origin_file = find_row_by_name(driver, provider, new_file)
        destination_file = find_row_by_name(driver, 'osf', new_file)

        if modifier_key == 'alt':
            # test for copy
            assert 'drag_this_file.txt' in origin_file.text
            assert 'drag_this_file.txt' in destination_file.text
        else:
            # test for move
            assert origin_file is None
            assert 'drag_this_file.txt' in destination_file.text

        try:
            # Attempt to delete drag_this_file.txt in origin provider folder
            osf_api.delete_file(session, metadata['data']['links']['delete'])
        except:
            print('No file to be deleted')

    @pytest.mark.parametrize('provider', ['dropbox'])
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

        row = find_row_by_name(driver, provider, new_file)
        row.click()
        download_button = find_toolbar_button_by_name(driver, 'Download')
        download_button.click()
        time.sleep(7)

        # Negative test
        assert 'Could not retrieve file or directory' not in driver.find_element_by_xpath('/html/body').text

        osf_api.delete_file(session, metadata['data']['links']['delete'])
