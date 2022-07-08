import datetime
import os

import pytest
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


def find_row_by_name(files_page, file_name):
    all_files = files_page.file_rows
    for file_row in all_files:
        if file_name in file_row.text:
            return file_row
    return


def connect_addon_to_node(session, provider, node_id):
    """Use the api to connect a storage addon provider to a project node."""
    addon = osf_api.get_user_addon(session, provider)
    addon_account_id = list(addon['data']['links']['accounts'])[0]
    osf_api.connect_provider_root_to_node(
        session, provider, addon_account_id, node_id=node_id
    )


@markers.dont_run_on_prod
@pytest.mark.usefixtures('must_be_logged_in')
class TestFilesPage:
    """We want to wrap all of our tests with try/finally so we can delete leftover files
    after failures. Decorators did not work here because we would need to pull out
    node_id from each test.
    """

    @pytest.mark.parametrize(
        'provider', ['box', 'dropbox', 'osfstorage', 'owncloud', 's3']
    )
    def test_rename_file(self, driver, default_project, session, provider):
        """Test that renames a single file from one of the storage providers on the
        Project Files List page.
        """
        current_browser = find_current_browser(driver)
        node_id = default_project.id
        if provider != 'osfstorage':
            connect_addon_to_node(session, provider, node_id)
        node = osf_api.get_node(session, node_id=node_id)
        # Upload a single test file to be renamed
        file_name = 'rename_' + current_browser + '_' + provider + '.txt'
        new_file, metadata = osf_api.upload_fake_file(
            session=session, node=node, name=file_name, provider=provider
        )
        try:
            files_page = FilesPage(driver, guid=node_id, addon_provider=provider)
            files_page.goto()
            # Wait for File List items to load
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '[data-test-file-list-item]')
                )
            )
            row = find_row_by_name(files_page, new_file)
            # Once we have found the right row we need to click the File Action menu
            # button at the far right side of the row to show the menu options. Then we
            # can click the Rename option from this menu.
            menu_button = row.find_element_by_css_selector(
                '[data-test-file-download-share-trigger]'
            )
            menu_button.click()
            rename_button = row.find_element_by_css_selector('[data-test-rename-link]')
            rename_button.click()
            # Delete the old file name from the input box
            for _ in range(len(new_file)):
                files_page.rename_file_modal.rename_input_box.send_keys(Keys.BACKSPACE)
            # Enter new file name in input box and click Save button
            new_name = current_browser + '_' + provider + '_renamed.txt'
            files_page.rename_file_modal.rename_input_box.send_keys_deliberately(
                new_name
            )
            files_page.rename_file_modal.save_button.click()
            # Need to wait for the Rename modal to disappear
            WebDriverWait(driver, 5).until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, '[data-test-file-rename-modal]')
                )
            )
            # The page is automatically reloaded with the new file name, so wait for the
            # list items to reappear.
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '[data-test-file-list-item]')
                )
            )
            # Test old file name does not exist
            old_file = find_row_by_name(files_page, new_file)
            assert old_file is None
            # Test that new file name is present and visible
            renamed_file = find_row_by_name(files_page, new_name)
            assert new_name in renamed_file.text
        finally:
            osf_api.delete_addon_files(session, provider, current_browser, guid=node_id)

    @pytest.mark.parametrize(
        'provider', ['box', 'dropbox', 'osfstorage', 'owncloud', 's3']
    )
    def test_delete_single_file(self, driver, default_project, session, provider):
        """Test that deletes a single file from one of the storage providers on the
        Project Files List page.
        """
        current_browser = driver.desired_capabilities.get('browserName')
        node_id = default_project.id
        if provider != 'osfstorage':
            connect_addon_to_node(session, provider, node_id)
        node = osf_api.get_node(session, node_id=node_id)
        # Upload a single test file to be deleted
        file_name = 'delete_' + current_browser + '_' + provider + '.txt'
        new_file, metadata = osf_api.upload_fake_file(
            session=session, node=node, name=file_name, provider=provider
        )
        try:
            files_page = FilesPage(driver, guid=node_id, addon_provider=provider)
            files_page.goto()
            # Wait for File List items to load
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '[data-test-file-list-item]')
                )
            )
            row = find_row_by_name(files_page, new_file)
            # Once we have found the right row we need to click the File Action menu
            # button at the far right side of the row to show the menu options. Then we
            # can click the Delete option from this menu.
            menu_button = row.find_element_by_css_selector(
                '[data-test-file-download-share-trigger]'
            )
            menu_button.click()
            delete_button = row.find_element_by_css_selector(
                '[data-test-delete-button]'
            )
            delete_button.click()
            # Click the Delete button on the modal
            files_page.delete_modal.delete_button[0].click()
            files_page.loading_indicator.here_then_gone()
            # Verify file has been deleted from the files list
            deleted_row = find_row_by_name(files_page, new_file)
            assert deleted_row is None
        finally:
            osf_api.delete_addon_files(session, provider, current_browser, guid=node_id)

    @pytest.mark.parametrize(
        'provider', ['box', 'dropbox', 'osfstorage', 'owncloud', 's3']
    )
    def test_delete_multiple_files(self, driver, default_project, session, provider):
        """Test that deletes multiple files (2) from one of the storage providers on the
        Project Files List page.
        """
        current_browser = driver.desired_capabilities.get('browserName')
        node_id = default_project.id
        if provider != 'osfstorage':
            connect_addon_to_node(session, provider, node_id)
        node = osf_api.get_node(session, node_id=node_id)
        # Upload 2 separate test files to be deleted
        file_name_1 = 'delete_1_' + current_browser + '_' + provider + '.txt'
        new_file_1, metadata = osf_api.upload_fake_file(
            session=session, node=node, name=file_name_1, provider=provider
        )
        file_name_2 = 'delete_2_' + current_browser + '_' + provider + '.txt'
        new_file_2, metadata = osf_api.upload_fake_file(
            session=session, node=node, name=file_name_2, provider=provider
        )
        try:
            files_page = FilesPage(driver, guid=node_id, addon_provider=provider)
            files_page.goto()
            # Wait for File List items to load
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '[data-test-file-list-item]')
                )
            )
            # Find the row for the 1st file to be deleted and click to select it
            row_1 = find_row_by_name(files_page, new_file_1)
            row_1.click()
            # Next find the 2nd file row and click it as well.
            row_2 = find_row_by_name(files_page, new_file_2)
            row_2.click()
            # Verify that 2 files have been selected
            assert files_page.file_selected_text.text == '2 item(s) selected'
            # Click the Delete button above the file list
            files_page.file_list_delete_button.click()
            # Click the Delete button on the modal
            files_page.delete_modal.delete_button[1].click()
            # Wait for Delete button to disappear
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        'div._Footer_gyio2l > button._Button_6kisxq._MediumButton_6kisxq._DestroyButton_6kisxq',
                    )
                )
            )
            # Verify success message on modal and click the Done button
            assert (
                files_page.delete_modal.heading.text == '2 items deleted successfully'
            )
            files_page.delete_modal.done_button.click()
            files_page.loading_indicator.here_then_gone()
            # Verify both files have been deleted from the files list
            deleted_row_1 = find_row_by_name(files_page, new_file_1)
            assert deleted_row_1 is None
            deleted_row_2 = find_row_by_name(files_page, new_file_2)
            assert deleted_row_2 is None
        finally:
            osf_api.delete_addon_files(session, provider, current_browser, guid=node_id)

    @pytest.mark.parametrize('provider', ['box', 'dropbox', 'owncloud', 's3'])
    def test_move_single_file(self, driver, default_project, session, provider):
        """Test that moves a single file from one of the storage providers on the
        Project Files List page to OSF Storage.
        """
        current_browser = driver.desired_capabilities.get('browserName')
        node_id = default_project.id
        if provider != 'osfstorage':
            connect_addon_to_node(session, provider, node_id)
        node = osf_api.get_node(session, node_id=node_id)
        # Upload a single test file to be moved
        file_name = 'move_' + current_browser + '_' + provider + '.txt'
        new_file, metadata = osf_api.upload_fake_file(
            session=session, node=node, name=file_name, provider=provider
        )
        try:
            files_page = FilesPage(driver, guid=node_id, addon_provider=provider)
            files_page.goto()
            # Wait for File List items to load
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '[data-test-file-list-item]')
                )
            )
            row = find_row_by_name(files_page, new_file)
            # Once we have found the right row we need to click the File Action menu
            # button at the far right side of the row to show the menu options. Then we
            # can click the Move option from this menu.
            menu_button = row.find_element_by_css_selector(
                '[data-test-file-download-share-trigger]'
            )
            menu_button.click()
            move_button = row.find_element_by_css_selector('[data-test-move-button]')
            move_button.click()
            # Click the Project link on the Move modal to go up a level and then click
            # the OSF Storage link. Then click the Move button on the modal to move
            # the file to OSF Storage.
            files_page.move_copy_modal.project_link.click()
            files_page.move_copy_modal.provider_osfstorage_link.click()
            files_page.move_copy_modal.move_copy_button.click()
            # After the move process has finished click the Done button to go back to
            # the Files list page.
            WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '[data-test-move-done-button]')
                )
            )
            files_page.move_copy_modal.done_button.click()
            files_page.loading_indicator.here_then_gone()
            # We should still be on the page for the provider, so check that the file
            # is no longer listed here.
            moved_row = find_row_by_name(files_page, new_file)
            assert moved_row is None
            # Click the link in the left navbar to switch to OSF Storage and verify the
            # file has been moved there.
            files_page.leftnav_osfstorage_link.click()
            files_page.loading_indicator.here_then_gone()
            moved_row = find_row_by_name(files_page, new_file)
            assert new_file in moved_row.text
        finally:
            osf_api.delete_addon_files(session, provider, current_browser, guid=node_id)

    @pytest.mark.parametrize('provider', ['box', 'dropbox', 'owncloud', 's3'])
    def test_move_multiple_files(self, driver, default_project, session, provider):
        """Test that moves multiple files from one of the storage providers on the
        Project Files List page to OSF Storage.
        """
        current_browser = driver.desired_capabilities.get('browserName')
        node_id = default_project.id
        if provider != 'osfstorage':
            connect_addon_to_node(session, provider, node_id)
        node = osf_api.get_node(session, node_id=node_id)
        # Upload 2 separate test files to be moved
        file_name_1 = 'move_1_' + current_browser + '_' + provider + '.txt'
        new_file_1, metadata = osf_api.upload_fake_file(
            session=session, node=node, name=file_name_1, provider=provider
        )
        file_name_2 = 'move_2_' + current_browser + '_' + provider + '.txt'
        new_file_2, metadata = osf_api.upload_fake_file(
            session=session, node=node, name=file_name_2, provider=provider
        )
        try:
            files_page = FilesPage(driver, guid=node_id, addon_provider=provider)
            files_page.goto()
            # Wait for File List items to load
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '[data-test-file-list-item]')
                )
            )
            # Find the row for the 1st file to be moved and click to select it
            row_1 = find_row_by_name(files_page, new_file_1)
            row_1.click()
            # Next find the 2nd file row and click it as well.
            row_2 = find_row_by_name(files_page, new_file_2)
            row_2.click()
            # Verify that 2 files have been selected
            assert files_page.file_selected_text.text == '2 item(s) selected'
            # Click the Move button above the file list
            files_page.file_list_move_button.click()
            # Click the Project link on the Move modal to go up a level and then click
            # the OSF Storage link. Then click the Move button on the modal to move
            # the file to OSF Storage.
            files_page.move_copy_modal.project_link.click()
            files_page.move_copy_modal.provider_osfstorage_link.click()
            files_page.move_copy_modal.loading_indicator.here_then_gone()
            files_page.move_copy_modal.move_copy_button.click()
            # After the move process has finished click the Done button to go back to
            # the Files list page.
            WebDriverWait(driver, 90).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '[data-test-move-done-button]')
                )
            )
            files_page.move_copy_modal.done_button.click()
            files_page.loading_indicator.here_then_gone()
            # We should still be on the page for the provider, so check that the files
            # are no longer listed here.
            moved_row_1 = find_row_by_name(files_page, new_file_1)
            assert moved_row_1 is None
            moved_row_2 = find_row_by_name(files_page, new_file_2)
            assert moved_row_2 is None
            # Click the link in the left navbar to switch to OSF Storage and verify the
            # files have been moved there.
            files_page.leftnav_osfstorage_link.click()
            files_page.loading_indicator.here_then_gone()
            moved_row_1 = find_row_by_name(files_page, new_file_1)
            assert new_file_1 in moved_row_1.text
            moved_row_2 = find_row_by_name(files_page, new_file_2)
            assert new_file_2 in moved_row_2.text
        finally:
            osf_api.delete_addon_files(session, provider, current_browser, guid=node_id)

    @pytest.mark.parametrize('provider', ['box', 'dropbox', 'owncloud', 's3'])
    def test_copy_single_file(self, driver, default_project, session, provider):
        """Test that copies a single file from one of the storage providers on the
        Project Files List page to OSF Storage.
        """
        current_browser = driver.desired_capabilities.get('browserName')
        node_id = default_project.id
        if provider != 'osfstorage':
            connect_addon_to_node(session, provider, node_id)
        node = osf_api.get_node(session, node_id=node_id)
        # Upload a single test file to be copied
        file_name = 'copy_' + current_browser + '_' + provider + '.txt'
        new_file, metadata = osf_api.upload_fake_file(
            session=session, node=node, name=file_name, provider=provider
        )
        try:
            files_page = FilesPage(driver, guid=node_id, addon_provider=provider)
            files_page.goto()
            # Wait for File List items to load
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '[data-test-file-list-item]')
                )
            )
            row = find_row_by_name(files_page, new_file)
            # Once we have found the right row we need to click the File Action menu
            # button at the far right side of the row to show the menu options. Then we
            # can click the Copy option from this menu.
            menu_button = row.find_element_by_css_selector(
                '[data-test-file-download-share-trigger]'
            )
            menu_button.click()
            move_button = row.find_element_by_css_selector('[data-test-copy-button]')
            move_button.click()
            # Click the Project link on the Copy modal to go up a level and then click
            # the OSF Storage link. Then click the Copy button on the modal to copy
            # the file to OSF Storage.
            files_page.move_copy_modal.project_link.click()
            files_page.move_copy_modal.provider_osfstorage_link.click()
            files_page.move_copy_modal.move_copy_button.click()
            # After the copy process has finished click the Done button to go back to
            # the Files list page.
            WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '[data-test-move-done-button]')
                )
            )
            files_page.move_copy_modal.done_button.click()
            files_page.loading_indicator.here_then_gone()
            # We should still be on the page for the provider, so check that the file
            # is still listed here.
            source_row = find_row_by_name(files_page, new_file)
            assert new_file in source_row.text
            # Click the link in the left navbar to switch to OSF Storage and verify the
            # file has been copied there.
            files_page.leftnav_osfstorage_link.click()
            files_page.loading_indicator.here_then_gone()
            destination_row = find_row_by_name(files_page, new_file)
            assert new_file in destination_row.text
        finally:
            osf_api.delete_addon_files(session, provider, current_browser, guid=node_id)

    @pytest.mark.parametrize('provider', ['box', 'dropbox', 'owncloud', 's3'])
    def test_copy_multiple_files(self, driver, default_project, session, provider):
        """Test that copies multiple files from one of the storage providers on the
        Project Files List page to OSF Storage.
        """
        current_browser = driver.desired_capabilities.get('browserName')
        node_id = default_project.id
        if provider != 'osfstorage':
            connect_addon_to_node(session, provider, node_id)
        node = osf_api.get_node(session, node_id=node_id)
        # Upload 2 separate test files to be moved
        file_name_1 = 'copy_1_' + current_browser + '_' + provider + '.txt'
        new_file_1, metadata = osf_api.upload_fake_file(
            session=session, node=node, name=file_name_1, provider=provider
        )
        file_name_2 = 'copy_2_' + current_browser + '_' + provider + '.txt'
        new_file_2, metadata = osf_api.upload_fake_file(
            session=session, node=node, name=file_name_2, provider=provider
        )
        try:
            files_page = FilesPage(driver, guid=node_id, addon_provider=provider)
            files_page.goto()
            # Wait for File List items to load
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '[data-test-file-list-item]')
                )
            )
            # Find the row for the 1st file to be copied and click to select it
            row_1 = find_row_by_name(files_page, new_file_1)
            row_1.click()
            # Next find the 2nd file row and click it as well.
            row_2 = find_row_by_name(files_page, new_file_2)
            row_2.click()
            # Verify that 2 files have been selected
            assert files_page.file_selected_text.text == '2 item(s) selected'
            # Click the Copy button above the file list
            files_page.file_list_copy_button.click()
            # Click the Project link on the Copy modal to go up a level and then click
            # the OSF Storage link. Then click the Copy button on the modal to copy
            # the file to OSF Storage.
            files_page.move_copy_modal.project_link.click()
            files_page.move_copy_modal.provider_osfstorage_link.click()
            files_page.move_copy_modal.loading_indicator.here_then_gone()
            files_page.move_copy_modal.move_copy_button.click()
            # After the copy process has finished click the Done button to go back to
            # the Files list page.
            WebDriverWait(driver, 90).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '[data-test-move-done-button]')
                )
            )
            files_page.move_copy_modal.done_button.click()
            files_page.loading_indicator.here_then_gone()
            # We should still be on the page for the provider, so check that the files
            # are still listed here.
            source_row_1 = find_row_by_name(files_page, new_file_1)
            assert new_file_1 in source_row_1.text
            source_row_2 = find_row_by_name(files_page, new_file_2)
            assert new_file_2 in source_row_2.text
            # Click the link in the left navbar to switch to OSF Storage and verify the
            # files have been copied there.
            files_page.leftnav_osfstorage_link.click()
            files_page.loading_indicator.here_then_gone()
            destination_row_1 = find_row_by_name(files_page, new_file_1)
            assert new_file_1 in destination_row_1.text
            destination_row_2 = find_row_by_name(files_page, new_file_2)
            assert new_file_2 in destination_row_2.text
        finally:
            osf_api.delete_addon_files(session, provider, current_browser, guid=node_id)

    @pytest.mark.parametrize(
        'provider', ['box', 'dropbox', 'osfstorage', 'owncloud', 's3']
    )
    def test_download_file(self, driver, default_project, session, provider):
        """Test that downloads a single file from one of the storage providers on the
        Project Files List page.
        """
        current_browser = driver.desired_capabilities.get('browserName')
        node_id = default_project.id
        if provider != 'osfstorage':
            connect_addon_to_node(session, provider, node_id)
        node = osf_api.get_node(session, node_id=node_id)
        # Upload a single test file to be downloaded
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
            files_page = FilesPage(driver, guid=node_id, addon_provider=provider)
            files_page.goto()
            # Wait for File List items to load
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '[data-test-file-list-item]')
                )
            )
            row = find_row_by_name(files_page, new_file)
            # Once we have found the right row we need to click the File Action menu
            # button at the far right side of the row to show the menu options. Then we
            # can click the Download option from this menu.
            menu_button = row.find_element_by_css_selector(
                '[data-test-file-download-share-trigger]'
            )
            menu_button.click()
            move_button = row.find_element_by_css_selector(
                '[data-test-download-button]'
            )
            move_button.click()
            # The actual file download usually takes a second or two, so instead of
            # using time.sleep() here we will just reload the page and wait for the
            # list items to reappear. That should be plenty of time.
            files_page.reload()
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '[data-test-file-list-item]')
                )
            )
            # Verify that the file is actually downloaded to user's machine
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
    Bitbucket - Read-only
    OneDrive - Similar issues to Google Drive. OneDrive is a special case that our API
                cannot currently handle.
    GitLab - Read-only
"""
