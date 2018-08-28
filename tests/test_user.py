import pytest
import markers
import settings

from api import osf_api
from pages.user import UserProfilePage

@pytest.fixture()
def quickfile(session):
    return osf_api.upload_single_quickfile(session)

@pytest.fixture
def user_one_profile_page(driver):
    profile_page = UserProfilePage(driver)
    return profile_page


# Generic class for testing a user profile
class ProfilePage:

    @markers.core_functionality
    def test_nothings_public(self, profile_page):
        """Confirm there the user has no public projects.
        """
        assert profile_page.no_public_projects_text.present()
        assert profile_page.no_public_components_text.present()

        if settings.PRODUCTION:
            assert profile_page.no_public_quickfiles.present()

    @markers.dont_run_on_prod
    def test_public_lists(self, quickfile, public_project, profile_page):
        profile_page.loading_indicator.here_then_gone()
        assert profile_page.quickfiles
        assert profile_page.public_projects


class TestProfileLoggedIn(ProfilePage):

    @pytest.fixture()
    def profile_page(self, user_one_profile_page, must_be_logged_in):
        user_one_profile_page.goto()
        return user_one_profile_page


class TestProfileLoggedOut(ProfilePage):

    @pytest.fixture()
    def profile_page(self, user_one_profile_page):
        user_one_profile_page.goto()
        return user_one_profile_page


class TestProfileAsDifferentUser(ProfilePage):

    @pytest.fixture()
    def profile_page(self, user_one_profile_page, must_be_logged_in_as_user_two):
        user_one_profile_page.goto()
        return user_one_profile_page
