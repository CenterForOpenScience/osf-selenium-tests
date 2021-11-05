import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import markers
from api import osf_api
from pages import user


@pytest.fixture()
def quickfile(session):
    return osf_api.upload_single_quickfile(session)


@pytest.fixture
def user_one_profile_page(driver):
    profile_page = user.UserProfilePage(driver)
    return profile_page


class ProfilePageMixin:
    """Mixin used to inject generic tests"""

    @pytest.fixture()
    def profile_page(self, driver):
        raise NotImplementedError()

    @markers.smoke_test
    @markers.core_functionality
    def test_nothings_public(self, profile_page):
        """Confirm that the user has no public projects."""
        profile_page.loading_indicator.here_then_gone()
        assert profile_page.no_public_projects_text.present()
        assert profile_page.no_public_components_text.present()

    @markers.dont_run_on_prod
    def test_public_lists(self, quickfile, public_project, profile_page):
        profile_page.loading_indicator.here_then_gone()
        assert profile_page.quickfiles
        assert profile_page.public_projects


class TestProfileLoggedIn(ProfilePageMixin):
    @pytest.fixture()
    def profile_page(self, user_one_profile_page, must_be_logged_in):
        user_one_profile_page.goto()
        return user_one_profile_page


class TestProfileLoggedOut(ProfilePageMixin):
    @pytest.fixture()
    def profile_page(self, user_one_profile_page):
        user_one_profile_page.goto()
        return user_one_profile_page


class TestProfileAsDifferentUser(ProfilePageMixin):
    @pytest.fixture()
    def profile_page(self, user_one_profile_page, must_be_logged_in_as_user_two):
        user_one_profile_page.goto()
        return user_one_profile_page


@pytest.mark.usefixtures('must_be_logged_in')
class TestUserSettings:
    @pytest.fixture(
        params=[
            user.ProfileInformationPage,
            user.AccountSettingsPage,
            user.ConfigureAddonsPage,
            user.NotificationsPage,
            user.DeveloperAppsPage,
            user.PersonalAccessTokenPage,
        ]
    )
    def settings_page(self, request, driver):
        """Run any test using this fixture with each user settings page individually."""
        settings_page = request.param(driver)
        return settings_page

    @pytest.fixture()
    def profile_settings_page(self, driver):
        profile_settings_page = user.ProfileInformationPage(driver)
        profile_settings_page.goto()
        return profile_settings_page

    @markers.smoke_test
    @markers.core_functionality
    def test_user_settings_loads(self, settings_page):
        """Confirm the given user settings page loads."""
        settings_page.goto()

    @markers.core_functionality
    def test_change_middle_name(self, driver, profile_settings_page, fake):
        new_name = fake.name()
        assert (
            profile_settings_page.middle_name_input.get_attribute('value') != new_name
        )
        profile_settings_page.middle_name_input.clear()
        profile_settings_page.middle_name_input.send_keys(new_name)
        profile_settings_page.save_button.click()
        profile_settings_page.update_success.here_then_gone()
        profile_settings_page.reload()
        assert WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element_value(
                (By.CSS_SELECTOR, '#names > div > form > div:nth-child(5) > input'),
                new_name,
            )
        )
