import os

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import markers
import settings
from api import osf_api
from pages import user


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
    @markers.core_functionality
    def test_public_lists(self, public_project, profile_page):
        profile_page.loading_indicator.here_then_gone()
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

    def test_user_settings_create_dev_app(self, driver, session, fake):
        """Create a Developer Application from the User Settings Developer Apps page
        in OSF. The test uses the OSF api to delete the developer app at the end of the
        test as cleanup.
        """
        dev_apps_page = user.DeveloperAppsPage(driver)
        dev_apps_page.goto()
        assert user.DeveloperAppsPage(driver, verify=True)
        dev_apps_page.create_dev_app_button.click()
        create_dev_app_page = user.CreateDeveloperAppPage(driver, verify=True)
        # Complete the form fields and click the Create developer app button
        app_name = fake.sentence(nb_words=3)
        create_dev_app_page.app_name_input.send_keys(app_name)
        create_dev_app_page.project_url_input.send_keys(settings.OSF_HOME)
        create_dev_app_page.app_description_textarea.click()
        create_dev_app_page.app_description_textarea.send_keys(
            'Selenium test: ' + os.environ['PYTEST_CURRENT_TEST']
        )
        create_dev_app_page.callback_url_input.send_keys('https://www.google.com/')
        create_dev_app_page.create_dev_app_button.click()
        try:
            # Verify that you are now on the Edit page for the newly created Developer
            # app
            edit_dev_app_page = user.EditDeveloperAppPage(driver, verify=True)
            edit_dev_app_page.loading_indicator.here_then_gone()
            # Get client id from the input box and verify that it is also in the page's
            # url
            client_id = edit_dev_app_page.client_id_input.get_attribute('value')
            assert client_id in driver.current_url
            # Verify other info on this page - we need to use up 2 minutes before
            # attempting to delete the dev app using the api, since CAS only refreshes
            # its db connection every 2 minutes.
            edit_dev_app_page.show_client_secret_button.click()
            # Get the dev app data from the api and verify client secret
            dev_app_data = osf_api.get_user_developer_app_data(
                session, app_id=client_id
            )
            client_secret = dev_app_data['attributes']['client_secret']
            assert (
                edit_dev_app_page.client_secret_input.get_attribute('value')
                == client_secret
            )
            edit_dev_app_page.scroll_into_view(edit_dev_app_page.app_name_input.element)
            assert edit_dev_app_page.app_name_input.get_attribute('value') == app_name
            edit_dev_app_page.scroll_into_view(
                edit_dev_app_page.project_url_input.element
            )
            assert (
                edit_dev_app_page.project_url_input.get_attribute('value')
                == settings.OSF_HOME
            )
            edit_dev_app_page.scroll_into_view(
                edit_dev_app_page.app_description_textarea.element
            )
            assert (
                edit_dev_app_page.app_description_textarea.get_attribute('value')
                == 'Selenium test: ' + os.environ['PYTEST_CURRENT_TEST']
            )
            edit_dev_app_page.scroll_into_view(
                edit_dev_app_page.callback_url_input.element
            )
            assert (
                edit_dev_app_page.callback_url_input.get_attribute('value')
                == 'https://www.google.com/'
            )
            # Click the Save button to go back to the Dev Apps list page
            edit_dev_app_page.scroll_into_view(edit_dev_app_page.save_button.element)
            edit_dev_app_page.save_button.click()
            dev_apps_page = user.DeveloperAppsPage(driver, verify=True)
            dev_apps_page.loading_indicator.here_then_gone()
            # Go through the list of developer apps listed on the page to find the one
            # that was just added
            dev_app_card = dev_apps_page.get_dev_app_card_by_app_name(app_name)
            app_link = dev_app_card.find_element_by_css_selector('a')
            link_url = app_link.get_attribute('href')
            link_client_id = link_url.split('applications/', 1)[1]
            assert link_client_id == client_id
            # Now click the app name link to go back to Edit Dev App page and verify
            # the data again - just trying to waste more time before we can delete
            # the app
            app_link.click()
            edit_dev_app_page = user.EditDeveloperAppPage(driver, verify=True)
            edit_dev_app_page.loading_indicator.here_then_gone()
            # Click the Show client secret button to unveil the client secret
            edit_dev_app_page.show_client_secret_button.click()
            # Verify text on the button has changed to 'Hide client secret'
            assert (
                edit_dev_app_page.show_client_secret_button.text == 'Hide client secret'
            )
            assert (
                edit_dev_app_page.client_secret_input.get_attribute('value')
                == client_secret
            )
            edit_dev_app_page.scroll_into_view(edit_dev_app_page.app_name_input.element)
            assert edit_dev_app_page.app_name_input.get_attribute('value') == app_name
            edit_dev_app_page.scroll_into_view(
                edit_dev_app_page.project_url_input.element
            )
            assert (
                edit_dev_app_page.project_url_input.get_attribute('value')
                == settings.OSF_HOME
            )
            edit_dev_app_page.scroll_into_view(
                edit_dev_app_page.app_description_textarea.element
            )
            assert (
                edit_dev_app_page.app_description_textarea.get_attribute('value')
                == 'Selenium test: ' + os.environ['PYTEST_CURRENT_TEST']
            )
            edit_dev_app_page.scroll_into_view(
                edit_dev_app_page.callback_url_input.element
            )
            assert (
                edit_dev_app_page.callback_url_input.get_attribute('value')
                == 'https://www.google.com/'
            )
            edit_dev_app_page.scroll_into_view(edit_dev_app_page.save_button.element)
            edit_dev_app_page.save_button.click()
            dev_apps_page = user.DeveloperAppsPage(driver, verify=True)
            dev_apps_page.loading_indicator.here_then_gone()
        finally:
            # Lastly use the api to delete the dev app as cleanup
            osf_api.delete_user_developer_app(session, app_id=client_id)
