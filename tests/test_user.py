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

    def test_user_settings_delete_dev_app(self, driver, session, fake):
        """Delete a Developer Application from the User Settings Developer Apps page
        in OSF. The test uses the OSF api to first create the developer application that
        will then be deleted using the Front End interface.
        """
        app_name = 'Dev App via api ' + fake.sentence(nb_words=1)
        app_id = osf_api.create_user_developer_app(
            session,
            name=app_name,
            description='a developer application created using the OSF api',
            home_url=settings.OSF_HOME,
            callback_url='https://www.google.com/',
        )
        # Note: We need to use up 2 minutes before attempting to delete the dev app
        # since CAS only refreshes its db connection every 2 minutes.
        try:
            # Go to the Profile Information page first and use the side navigation bar
            # to then go to the Developer Apps page.
            profile_settings_page = user.ProfileInformationPage(driver)
            profile_settings_page.goto()
            assert user.ProfileInformationPage(driver, verify=True)
            profile_settings_page.side_navigation.developer_apps_link.click()
            dev_apps_page = user.DeveloperAppsPage(driver, verify=True)
            dev_apps_page.loading_indicator.here_then_gone()
            # Go through the list of developer apps listed on the page to find the one
            # that was just added via the api
            dev_app_card = dev_apps_page.get_dev_app_card_by_app_name(app_name)
            app_link = dev_app_card.find_element_by_css_selector('a')
            link_url = app_link.get_attribute('href')
            link_client_id = link_url.split('applications/', 1)[1]
            assert link_client_id == app_id
            # Now click the app name link to go to the Edit Dev App page and verify the
            # data
            app_link.click()
            edit_dev_app_page = user.EditDeveloperAppPage(driver, verify=True)
            edit_dev_app_page.loading_indicator.here_then_gone()
            # Verify that the app_id is also in the page's url
            assert app_id in driver.current_url
            assert edit_dev_app_page.client_id_input.get_attribute('value') == app_id
            edit_dev_app_page.show_client_secret_button.click()
            # Get the dev app data from the api and verify client secret
            dev_app_data = osf_api.get_user_developer_app_data(session, app_id=app_id)
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
                == 'a developer application created using the OSF api'
            )
            edit_dev_app_page.scroll_into_view(
                edit_dev_app_page.callback_url_input.element
            )
            assert (
                edit_dev_app_page.callback_url_input.get_attribute('value')
                == 'https://www.google.com/'
            )
            # Note: The Delete button on the Edit Dev App page does not actually do
            # anything - this is a known bug. So click the Save button to go back to
            # the Dev Apps List page and delete the app from there.
            edit_dev_app_page.scroll_into_view(edit_dev_app_page.save_button.element)
            edit_dev_app_page.save_button.click()
            dev_apps_page = user.DeveloperAppsPage(driver, verify=True)
            dev_apps_page.loading_indicator.here_then_gone()
            dev_app_card = dev_apps_page.get_dev_app_card_by_app_name(app_name)
            delete_button = dev_app_card.find_element_by_css_selector(
                '[data-test-delete-button]'
            )
            delete_button.click()
            # Verify the Delete Dev App Modal is displayed
            delete_modal = dev_apps_page.delete_dev_app_modal
            assert delete_modal.app_name.text == app_name
            # Click the Cancel button first and verify that the Dev App is not
            # actually deleted
            delete_modal.cancel_button.click()
            dev_apps_page.reload()
            dev_apps_page = user.DeveloperAppsPage(driver, verify=True)
            dev_apps_page.loading_indicator.here_then_gone()
            # Find the Dev App card again and click the Delete button again
            dev_app_card = dev_apps_page.get_dev_app_card_by_app_name(app_name)
            delete_button = dev_app_card.find_element_by_css_selector(
                '[data-test-delete-button]'
            )
            delete_button.click()
            delete_modal = dev_apps_page.delete_dev_app_modal
            assert delete_modal.app_name.text == app_name
            # This time click the Delete button to actually delete the Dev App
            delete_modal.delete_button.click()
            dev_apps_page.reload()
            dev_apps_page = user.DeveloperAppsPage(driver, verify=True)
            dev_apps_page.loading_indicator.here_then_gone()
            dev_app_card = dev_apps_page.get_dev_app_card_by_app_name(app_name)
            # Verify that we don't find the dev app card this time since it was deleted
            assert not dev_app_card
        except Exception:
            # As cleanup, delete the dev app using the api if the test failed for some
            # reason and the dev app was not actually deleted.
            dev_app_data = osf_api.get_user_developer_app_data(session, app_id=app_id)
            if dev_app_data:
                osf_api.delete_user_developer_app(session, app_id=app_id)
