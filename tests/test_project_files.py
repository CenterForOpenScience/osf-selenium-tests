import datetime
import os
import time

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import markers
import settings
from api import osf_api
from pages.project import FilesPage
from utils import find_current_browser


"""
*** NOTE ***
For the test user running this test, the following addons must be manually
authorized in user settings, or else the test will fail to run:
    - 'box', 'dropbox', 's3', 'owncloud'
"""


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
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#tb-tbody div[data-level="3"]')
        )
    )
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, '#tb-tbody .fa-refresh'))
    )

    all_fangorn_rows = driver.find_elements_by_css_selector(
        '#treeGrid .tb-table .tb-tbody-inner > div > div'
    )
    fangorn_dictionary = {}
    key = ''

    for row in all_fangorn_rows:
        data_level = row.get_attribute('data-level')
        if data_level == '2':
            key = format_provider_name(row)
            fangorn_dictionary[key] = []
        elif data_level == '3':
            file_name = row.find_element_by_css_selector('.td-title .title-text')
            # Create sub-dictionary entries for each provider
            # Each sub-dictionary contains name of the row and the row object
            fangorn_dictionary[key].append(
                {'file_name': file_name.text, 'row_object': row}
            )

    return fangorn_dictionary


def find_row_by_name(driver, provider, row_name):
    all_files = create_dictionary(driver)
    for x in all_files[provider]:
        if x['file_name'] == row_name:
            return x['row_object']
    return


# Click a button in the toolbar, just pass in the button name
def find_toolbar_button_by_name(driver, button_name):
    file_action_buttons = driver.find_elements_by_css_selector(
        '#folderRow .fangorn-toolbar-icon'
    )
    for button in file_action_buttons:
        if button.text == button_name:
            return button
    return


@markers.dont_run_on_prod
@pytest.mark.usefixtures('must_be_logged_in')
class TestFilesPage:
    """We want to wrap all of our tests with try/finally so we can delete leftover files after failures.
    Decorators did not work here because we would need to pull out node_id from each test.
    """

    @pytest.mark.parametrize('provider', ['box', 'dropbox', 'owncloud', 's3'])
    def test_rename_file(self, driver, default_project, session, provider):
        current_browser = find_current_browser(driver)
        node_id = default_project.id

        # Connect addon to node, upload a single test file
        node = osf_api.get_node(session, node_id=node_id)
        if provider != 'osfstorage':
            addon = osf_api.get_user_addon(session, provider)
            addon_account_id = list(addon['data']['links']['accounts'])[0]
            osf_api.connect_provider_root_to_node(
                session, provider, addon_account_id, node_id=node_id
            )

        file_name = 'rename_' + current_browser + '_' + provider + '.txt'
        new_file, metadata = osf_api.upload_fake_file(
            session=session, node=node, name=file_name, provider=provider
        )

        try:
            files_page = FilesPage(driver, guid=node_id)
            files_page.goto()

            row = find_row_by_name(driver, provider, new_file)
            row.click()
            rename_button = find_toolbar_button_by_name(driver, 'Rename')
            rename_button.click()
            rename_text_box = driver.find_element_by_id('renameInput')

            for _ in range(len(new_file)):
                rename_text_box.send_keys(Keys.BACKSPACE)

            new_name = current_browser + '_' + provider + '_renamed.txt'
            rename_text_box.send_keys(new_name)
            rename_text_box.send_keys(Keys.RETURN)

            # Wait for 5 seconds for Rename message to show
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'text-muted'))
            )
            # Wait a maximum of 20 seconds for Rename message to resolve
            WebDriverWait(driver, 20).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, 'text-muted'))
            )

            files_page.goto()
            # Test old file name does not exist
            old_file = find_row_by_name(driver, provider, file_name)
            assert old_file is None

            # Test that new file name is present and visible
            renamed_file = find_row_by_name(driver, provider, new_name)
            assert new_name in renamed_file.text

        finally:
            osf_api.delete_addon_files(session, provider, current_browser, guid=node_id)

    @markers.core_functionality
    def test_checkout_file(self, driver, default_project, session):
        current_browser = driver.desired_capabilities.get('browserName')
        node_id = default_project.id
        provider = 'osfstorage'

        # Connect add-on to node, upload a single test file
        node = osf_api.get_node(session, node_id=node_id)
        file_name = 'checkout_' + find_current_browser(driver) + '.txt'
        new_file, metadata = osf_api.upload_fake_file(
            session=session, node=node, name=file_name, provider=provider
        )

        try:
            files_page = FilesPage(driver, guid=node_id)
            files_page.goto()

            row = find_row_by_name(driver, 'osf', new_file)
            row.click()
            checkout_button = find_toolbar_button_by_name(driver, 'Check out file')
            checkout_button.click()
            # Accept the confirmation modal
            driver.find_element_by_css_selector('.btn-warning').click()

            # Wait for delete modal to resolve
            WebDriverWait(driver, 5).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, '.btn-warning'))
            )
            # Wait for 3rd fangorn row to load
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '#tb-tbody > div > div > div:nth-child(3)')
                )
            )

            # Test that Check Out button is no longer present
            row = find_row_by_name(driver, 'osf', new_file)
            row.click()
            checkout_button = find_toolbar_button_by_name(driver, 'Check out file')
            assert checkout_button is None

            row = find_row_by_name(driver, 'osf', new_file)
            row.click()
            check_in_button = find_toolbar_button_by_name(driver, 'Check in file')
            check_in_button.click()

            # Wait for page to reload
            WebDriverWait(driver, 5).until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, '#tb-tbody > div > div > div:nth-child(3)')
                )
            )
            # Wait for 3rd fangorn row to load
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '#tb-tbody > div > div > div:nth-child(3)')
                )
            )

            # Test that Check In button is no longer present
            row = find_row_by_name(driver, 'osf', new_file)
            row.click()
            check_in_button = find_toolbar_button_by_name(driver, 'Check in file')
            assert check_in_button is None

        finally:
            osf_api.delete_addon_files(session, provider, current_browser, guid=node_id)

    @markers.core_functionality
    @pytest.mark.parametrize('provider', ['box', 'dropbox', 'owncloud', 's3'])
    def test_delete_file(self, driver, default_project, session, provider):
        current_browser = driver.desired_capabilities.get('browserName')
        node_id = default_project.id

        # Connect addon to node, upload a single test file
        node = osf_api.get_node(session, node_id=node_id)
        if provider != 'osfstorage':
            addon = osf_api.get_user_addon(session, provider)
            addon_account_id = list(addon['data']['links']['accounts'])[0]
            osf_api.connect_provider_root_to_node(
                session, provider, addon_account_id, node_id=node_id
            )

        file_name = 'delete_' + current_browser + '_' + provider + '.txt'
        new_file, metadata = osf_api.upload_fake_file(
            session=session, node=node, name=file_name, provider=provider
        )

        try:
            files_page = FilesPage(driver, guid=node_id)
            files_page.goto()

            row = find_row_by_name(driver, provider, new_file)
            row.click()
            delete_button = find_toolbar_button_by_name(driver, 'Delete')
            delete_button.click()

            # Wait for the delete confirmation
            files_page.delete_modal.present()

            # Front End will show 'delete failed' message - still works as expected
            driver.find_element_by_css_selector('.btn-danger').click()

            # Wait for delete modal to resolve
            WebDriverWait(driver, 5).until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, 'p[class="text-danger"]')
                )
            )

            deleted_row = find_row_by_name(driver, provider, new_file)
            assert deleted_row is None

        finally:
            osf_api.delete_addon_files(session, provider, current_browser, guid=node_id)

    @pytest.mark.parametrize(
        'provider, modifier_key, action',
        [
            ['s3', 'none', 'move'],
            ['s3', 'alt', 'copy'],
            ['box', 'none', 'move'],
            ['box', 'alt', 'copy'],
            ['dropbox', 'none', 'move'],
            ['dropbox', 'alt', 'copy'],
            ['owncloud', 'none', 'move'],
            ['owncloud', 'alt', 'copy'],
        ],
    )
    def test_dragon_drop(
        self, driver, default_project, session, provider, modifier_key, action
    ):
        current_browser = driver.desired_capabilities.get('browserName')
        node_id = default_project.id

        # Connect addon to node, upload a single test file
        node = osf_api.get_node(session, node_id=node_id)
        if provider != 'osfstorage':
            addon = osf_api.get_user_addon(session, provider)
            addon_account_id = list(addon['data']['links']['accounts'])[0]
            osf_api.connect_provider_root_to_node(
                session, provider, addon_account_id, node_id=node_id
            )
        if modifier_key == 'alt':
            file_name = 'copy_' + find_current_browser(driver) + '_' + provider + '.txt'
            new_file, metadata = osf_api.upload_fake_file(
                session=session, node=node, name=file_name, provider=provider
            )
        else:
            file_name = 'move_' + current_browser + '_' + provider + '.txt'
            new_file, metadata = osf_api.upload_fake_file(
                session=session, node=node, name=file_name, provider=provider
            )

        try:
            files_page = FilesPage(driver, guid=node_id)
            files_page.goto()

            # Find the row that contains the new file
            source_row = find_row_by_name(driver, provider, new_file)

            # Find the row with the OSF storage
            for row in files_page.fangorn_addons:
                if row.text == 'OSF Storage (United States)':
                    target = row
                    break

            action_chains = ActionChains(driver)
            action_chains.reset_actions()

            if 'firefox' in current_browser:
                if modifier_key == 'alt':
                    # Copy file
                    action_chains.key_down(Keys.LEFT_ALT).perform()
                    action_chains.drag_and_drop(source_row, target).perform()
                else:
                    # Move file
                    action_chains.drag_and_drop(source_row, target).perform()
            else:
                # The sleeps in the following code block are needed for
                # Chromium's virtual keyboard to work properly
                if modifier_key == 'alt':
                    # Copy file
                    time.sleep(1)
                    action_chains.key_down(Keys.ALT).perform()
                    time.sleep(1)
                    action_chains.click_and_hold(source_row).perform()
                    time.sleep(1)
                    action_chains.drag_and_drop(source_row, target).perform()
                    time.sleep(1)
                    action_chains.reset_actions()
                    if 'chrome' in current_browser:
                        # The ALT key_up seems to be necessary for Chrome. Without it
                        # every other copy attempt actually becomes a move.
                        action_chains.key_up(Keys.ALT).perform()
                        time.sleep(1)
                        # However, the ALT key_up can cause an unwanted repetition of
                        # the drag and drop action which can cause a pop-up modal about
                        # replacing the copied file. This seems to happen most often
                        # on BrowserStack.  If we see this modal, then close it.
                        if files_page.replace_modal.present():
                            files_page.replace_modal_close_button.click()
                else:
                    # Move file
                    action_chains.click_and_hold(source_row).perform()
                    # Chrome -> will highlight multiple rows if you do not sleep here
                    time.sleep(1)
                    action_chains.drag_and_drop(source_row, target).perform()

            try:
                # Wait for 5 seconds for Copying message to show
                WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, 'text-muted'))
                )
            except TimeoutException:
                pass

            try:
                # Wait a maximum of 30 seconds for Copying message to resolve
                WebDriverWait(driver, 30).until(
                    EC.invisibility_of_element_located((By.CLASS_NAME, 'text-muted'))
                )
            except TimeoutException:
                # Reload the page and continue test
                pass

            files_page.goto()
            origin_file = find_row_by_name(driver, provider, new_file)
            destination_file = find_row_by_name(driver, 'osf', new_file)

            if modifier_key == 'alt':
                # Test for copy
                assert 'copy' in origin_file.text
                assert 'copy' in destination_file.text

                osf_api.delete_file(session, metadata['data']['links']['delete'])

            else:
                # Test for move
                assert origin_file is None
                assert 'move' in destination_file.text

        finally:
            osf_api.delete_addon_files(session, provider, current_browser, guid=node_id)

    @pytest.mark.parametrize('provider', ['s3', 'dropbox', 'box', 'owncloud'])
    def test_download_file(self, driver, default_project, session, provider):
        current_browser = driver.desired_capabilities.get('browserName')
        node_id = default_project.id

        # Connect addon to node, upload a single test file
        node = osf_api.get_node(session, node_id=node_id)
        if provider != 'osfstorage':
            addon = osf_api.get_user_addon(session, provider)
            addon_account_id = list(addon['data']['links']['accounts'])[0]
            osf_api.connect_provider_root_to_node(
                session, provider, addon_account_id, node_id=node_id
            )

        file_name = 'download_' + current_browser + '_' + provider + '.txt'
        new_file, metadata = osf_api.upload_fake_file(
            session=session, node=node, name=file_name, provider=provider
        )

        try:
            # If running on local machine, first check if the download file already
            # exists in the Downloads folder. If so then delete the old copy before
            # attempting to download a new one.
            if settings.DRIVER != 'Remote':
                file_path = os.path.expanduser('~/Downloads/' + file_name)
                if os.path.exists(file_path):
                    os.remove(file_path)

            files_page = FilesPage(driver, guid=node_id)
            files_page.goto()

            row = find_row_by_name(driver, provider, new_file)
            row.click()
            download_button = find_toolbar_button_by_name(driver, 'Download')
            download_button.click()
            # Wait to see if error message appears -- for negative test
            time.sleep(2)

            # Negative test
            assert (
                'Could not retrieve file or directory'
                not in driver.find_element_by_xpath('/html/body').text
            )

            # Positive Test: Verify that file is actually downloaded to user's machine
            current_date = datetime.datetime.now()
            if settings.DRIVER == 'Remote':
                # First verify the downloaded file exists on the virtual remote machine
                assert driver.execute_script(
                    'browserstack_executor: {"action": "fileExists", "arguments": {"fileName": "%s"}}'
                    % (file_name)
                )
                # Next get the file properties and then verify that the file creation date is today
                file_props = driver.execute_script(
                    'browserstack_executor: {"action": "getFileProperties", "arguments": {"fileName": "%s"}}'
                    % (file_name)
                )
                file_create_date = datetime.datetime.fromtimestamp(
                    file_props['created_time']
                )
                assert file_create_date.date() == current_date.date()
            else:
                # First verify the downloaded file exists
                assert os.path.exists(file_path)
                # Next verify the file was downloaded today
                file_mtime = os.path.getmtime(file_path)
                file_mod_date = datetime.datetime.fromtimestamp(file_mtime)
                assert file_mod_date.date() == current_date.date()

        finally:
            osf_api.delete_addon_files(session, provider, current_browser, guid=node_id)


"""
TODO:
- write an uploads test

Addons this test does not cover, and reasons:
    Google Drive - must specify both folder_id and folder_path
    Github - requested add-on not currently configurable via API
    Dataverse - requested add-on not currently configurable via API
    Figshare - has a non-conventional file setup not suited for normal file actions
"""
