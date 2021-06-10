import pytest
import markers
import re
from api import osf_api

from pages.quickfiles import QuickfilesPage, QuickfileDetailPage
from pages.project import ProjectPage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


@pytest.fixture()
def quickfiles_page(driver, session):
    osf_api.upload_single_quickfile(session)
    return QuickfilesPage(driver)


@markers.dont_run_on_prod
class TestQuickfilesLoggedIn:

    @pytest.fixture()
    def my_quickfiles(self, quickfiles_page, must_be_logged_in):
        quickfiles_page.goto()
        return quickfiles_page

    @markers.core_functionality
    def test_quickfile_exists(self, driver, my_quickfiles):
        my_quickfiles.loading_indicator.here_then_gone()
        my_quickfiles.file_titles[0].click()
        quickfileDetail = QuickfileDetailPage(driver, verify=True)

        # verify expected buttons on Quickfiles Detail page
        assert quickfileDetail.delete_button.present()
        assert quickfileDetail.download_button.present()
        assert quickfileDetail.share_button.present()
        assert quickfileDetail.view_button.present()
        assert quickfileDetail.edit_button.present()
        assert quickfileDetail.revisions_button.present()
        assert quickfileDetail.filter_button.present()

    def test_expected_buttons(self, my_quickfiles):
        # Check expected buttons when file is not selected
        assert my_quickfiles.upload_button.present()
        assert my_quickfiles.filter_button.present()
        assert my_quickfiles.help_button.present()
        assert my_quickfiles.download_as_zip_button.present()

        assert my_quickfiles.share_button.absent()
        assert my_quickfiles.download_button.absent()
        assert my_quickfiles.view_button.absent()
        assert my_quickfiles.move_button.absent()
        assert my_quickfiles.delete_button.absent()
        assert my_quickfiles.rename_button.absent()

        my_quickfiles.loading_indicator.here_then_gone()
        my_quickfiles.files[0].click()

        # Check expected buttons when file is selected
        assert my_quickfiles.upload_button.present()
        assert my_quickfiles.share_button.present()
        assert my_quickfiles.download_button.present()
        assert my_quickfiles.view_button.present()
        assert my_quickfiles.move_button.present()
        assert my_quickfiles.delete_button.present()
        assert my_quickfiles.rename_button.present()
        assert my_quickfiles.filter_button.present()
        assert my_quickfiles.help_button.present()

        assert my_quickfiles.download_as_zip_button.absent()

    def test_help_button(self, my_quickfiles):
        my_quickfiles.loading_indicator.here_then_gone()
        # click the Help button and verify modal window opens
        my_quickfiles.help_button.click()
        assert my_quickfiles.generic_modal.present()
        assert my_quickfiles.generic_modal.text == 'How to use the file browser'
        my_quickfiles.help_modal_close_button.click()

    def test_share_quickfile(self, my_quickfiles):
        my_quickfiles.loading_indicator.here_then_gone()
        my_quickfiles.files[0].click()
        # click the Share button and verify that popover box appears
        my_quickfiles.share_button.click()
        assert my_quickfiles.share_popover.present()

    def test_view_quickfile(self, driver, my_quickfiles):
        my_quickfiles.loading_indicator.here_then_gone()
        my_quickfiles.files[0].click()
        # click the View button and verify that you are navigated to Quickfiles Detail page
        my_quickfiles.view_button.click()
        QuickfileDetailPage(driver, verify=True)

    def test_filter_quickfile(self, my_quickfiles):
        my_quickfiles.loading_indicator.here_then_gone()
        my_quickfiles.filter_button.click()
        assert my_quickfiles.filter_input.present()
        my_quickfiles.filter_input.click()
        # enter a value in the filter input box that wll filter out the file from the list
        my_quickfiles.filter_input.send_keys_deliberately('XXXXXX')
        assert EC.invisibility_of_element_located((By.CSS_SELECTOR, '[data-test-file-icon-and-name]'))
        # clear the filter input box and verify that the file is visible again
        for _ in range(5):
            my_quickfiles.filter_input.send_keys_deliberately(Keys.BACKSPACE)
        assert EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-test-file-icon-and-name]'))
        my_quickfiles.filter_close_button.click()

    def test_move_quickfile_to_new_project(self, driver, session, my_quickfiles):
        my_quickfiles.loading_indicator.here_then_gone()
        file_name = driver.find_element(By.CSS_SELECTOR, '[data-test-file-icon-and-name]').text
        my_quickfiles.files[0].click()
        my_quickfiles.move_button.click()
        # verify move modal
        assert my_quickfiles.generic_modal.present()
        assert my_quickfiles.generic_modal.text == 'Move file to project'
        assert my_quickfiles.move_create_new_project_button.present()
        assert my_quickfiles.move_existing_project_button.present()
        my_quickfiles.move_create_new_project_button.click()
        new_project_tile = 'OSF Selenium Test Quickfile Move'
        my_quickfiles.create_project_modal.title_input.send_keys(new_project_tile)
        my_quickfiles.create_project_modal.create_project_button.click()
        my_quickfiles.project_created_modal.go_to_project_href_link.click()
        project_page = ProjectPage(driver, verify=True)
        assert project_page.title.text == new_project_tile
        # Capture guid for project so we can delete it later
        match = re.search(r'osf\.io/([a-z0-9]{5})', driver.current_url)
        project_guid = match.group(1)
        # Verify that Quick File is listed in Project Files Widget
        project_page.file_widget.loading_indicator.here_then_gone()
        assert project_page.file_widget.component_and_file_titles[3].text == file_name
        # Go back to My Quick Files page and verify that file is no longer listed there
        my_quickfiles.goto()
        my_quickfiles.loading_indicator.here_then_gone()
        assert len(my_quickfiles.files) == 0
        # Cleanup - delete the new project
        osf_api.delete_project(session, project_guid, None)

    def test_delete_quickfile(self, my_quickfiles):
        my_quickfiles.loading_indicator.here_then_gone()
        my_quickfiles.files[0].click()
        my_quickfiles.delete_button.click()
        my_quickfiles.confirm_delete_button.click()
        my_quickfiles.flash_message.here_then_gone()
        assert len(my_quickfiles.files) == 0

    def test_rename_quickfile(self, driver, my_quickfiles):
        my_quickfiles.loading_indicator.here_then_gone()
        original_name = driver.find_element(By.CSS_SELECTOR, '[data-test-file-icon-and-name]').text
        my_quickfiles.files[0].click()
        my_quickfiles.rename_button.click()
        assert my_quickfiles.rename_input.present()
        my_quickfiles.rename_input.click()
        my_quickfiles.rename_input.clear()
        new_name = 'osf_selenium_test_renamed_quickfile.txt'
        assert original_name != new_name
        my_quickfiles.rename_input.send_keys_deliberately(new_name)
        my_quickfiles.rename_save_button.click()
        my_quickfiles.flash_message.here_then_gone()
        assert driver.find_element(By.CSS_SELECTOR, '[data-test-file-icon-and-name]').text == new_name


@markers.dont_run_on_prod
class AnothersQuickfilesMixin:
    """Mixin used to inject generic tests
    """
    @pytest.fixture()
    def anothers_quickfiles(self, quickfiles_page):
        raise NotImplementedError()

    @markers.core_functionality
    def test_quickfile_exists(self, driver, anothers_quickfiles):
        anothers_quickfiles.loading_indicator.here_then_gone()
        anothers_quickfiles.file_titles[0].click()
        quickfileDetail = QuickfileDetailPage(driver, verify=True)

        # verify expected buttons on Quickfiles Detail page
        assert quickfileDetail.delete_button.absent()
        assert quickfileDetail.download_button.present()
        assert quickfileDetail.share_button.present()
        assert quickfileDetail.view_button.present()
        assert quickfileDetail.edit_button.absent()
        assert quickfileDetail.revisions_button.present()
        assert quickfileDetail.filter_button.present()

    def test_expected_buttons(self, anothers_quickfiles):
        # Check expected buttons when file is not selected
        assert anothers_quickfiles.filter_button.present()
        assert anothers_quickfiles.help_button.present()
        assert anothers_quickfiles.download_as_zip_button.present()

        assert anothers_quickfiles.upload_button.absent()
        assert anothers_quickfiles.share_button.absent()
        assert anothers_quickfiles.download_button.absent()
        assert anothers_quickfiles.view_button.absent()
        assert anothers_quickfiles.move_button.absent()
        assert anothers_quickfiles.delete_button.absent()
        assert anothers_quickfiles.rename_button.absent()

        anothers_quickfiles.loading_indicator.here_then_gone()
        anothers_quickfiles.files[0].click()

        # Check expected buttons when file is selected
        assert anothers_quickfiles.filter_button.present()
        assert anothers_quickfiles.help_button.present()
        assert anothers_quickfiles.share_button.present()
        assert anothers_quickfiles.download_button.present()
        assert anothers_quickfiles.view_button.present()

        assert anothers_quickfiles.upload_button.absent()
        assert anothers_quickfiles.move_button.absent()
        assert anothers_quickfiles.delete_button.absent()
        assert anothers_quickfiles.rename_button.absent()

        assert anothers_quickfiles.download_as_zip_button.absent()


@markers.dont_run_on_prod
class TestQuickfilesLoggedOut(AnothersQuickfilesMixin):

    @pytest.fixture()
    def anothers_quickfiles(self, quickfiles_page):
        quickfiles_page.goto()
        return quickfiles_page


@markers.dont_run_on_prod
class TestQuickfilesAsDifferentUser(AnothersQuickfilesMixin):

    @pytest.fixture()
    def anothers_quickfiles(self, quickfiles_page, must_be_logged_in_as_user_two):
        quickfiles_page.goto()
        return quickfiles_page
