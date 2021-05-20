import pytest
import markers
from api import osf_api

from pages.quickfiles import QuickfilesPage, QuickfileDetailPage


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
        QuickfileDetailPage(driver, verify=True)

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
        QuickfileDetailPage(driver, verify=True)

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
