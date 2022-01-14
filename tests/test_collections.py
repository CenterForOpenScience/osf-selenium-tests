import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import markers
from api import osf_api
from pages.collections import (
    CollectionDiscoverPage,
    CollectionSubmitPage,
)
from pages.project import ProjectPage


@markers.smoke_test
class TestCollectionDiscoverPages:
    """This test will load the Discover page for each Collection Provider that exists in
    an environment.
    """

    def providers():
        """Return all collection providers."""
        return osf_api.get_providers_list(type='collections')

    @pytest.fixture(params=providers(), ids=[prov['id'] for prov in providers()])
    def provider(self, request):
        return request.param

    def test_discover_page(self, session, driver, provider):
        discover_page = CollectionDiscoverPage(driver, provider=provider)
        discover_page.goto()
        discover_page.loading_indicator.here_then_gone()
        assert CollectionDiscoverPage(driver, verify=True)


@markers.dont_run_on_prod
class TestCollectionSubmission:
    """This tests the process of submitting a project to a Collection via the Collection
    Submit page for a given provider.  We will be using a specific test collection
    reserved for Selenium testing in each of the testing environments and therefore we
    will not be running this test in the Production environment.
    """

    @pytest.fixture
    def provider(self, driver):
        return osf_api.get_provider(type='collections', provider_id='selenium')

    def test_add_to_collection(
        self,
        driver,
        session,
        provider,
        project_with_file,
        must_be_logged_in,
    ):
        try:
            submit_page = CollectionSubmitPage(driver, provider=provider)
            submit_page.goto()
            assert CollectionSubmitPage(driver, verify=True)
            # Select the dummmy project from the listbox in the Select a project section
            submit_page.project_selector.click()
            submit_page.project_help_text.here_then_gone()
            submit_page.project_selector_project.click()
            # Project metadata section - select a license, enter description, and add tag
            submit_page.scroll_into_view(submit_page.project_metadata_save.element)
            submit_page.license_dropdown_trigger.click()
            submit_page.first_license_option.click()
            submit_page.description_textbox.click()
            submit_page.description_textbox.send_keys_deliberately(
                'QA Selenium Testing'
            )
            submit_page.tags_input.click()
            submit_page.tags_input.send_keys('selenium\r')
            submit_page.project_metadata_save.click()
            # Project contributors section - just click Continue button
            WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '[data-test-project-contributors-list-item-name]')
                )
            )
            submit_page.scroll_into_view(
                submit_page.project_contributors_continue.element
            )
            submit_page.project_contributors_continue.click()
            # Collection metadata section - select from Type listbox and click Continue
            submit_page.type_dropdown_trigger.click()
            submit_page.first_type_option.click()
            submit_page.collection_metadata_continue.click()

            # Finally click the Add to collection button at the bottom of the form and on
            # the confirmation modal to complete the submission
            submit_page.add_to_collection_button.click()
            submit_page.modal_add_to_collection_button.click()
            # After submitting we will end up on the Project page - verify this and verify
            # there is a new section on Project page indicating the project is part of a
            # collection with a link to the collection.
            project_page = ProjectPage(driver, verify=True, guid=project_with_file.id)
            assert project_page.collections_container.present()
            assert provider['id'] in project_page.collections_link.get_attribute('href')
            # Also verify Project is now Public.
            assert project_page.make_private_link.present()
        finally:
            # If we are still stuck on the Collection Submit page then refresh it to see
            # if we get an alert pop-up message about leaving the page.  If so then
            # accept the alert so that we can get off this page and can proceed with
            # the rest of the tests.
            if submit_page.verify():
                submit_page.reload()
                try:
                    WebDriverWait(driver, 3).until(EC.alert_is_present())
                    driver.switch_to.alert.accept()
                except TimeoutException:
                    pass

            # Need to make project Private to get it to disappear from Collection Discover
            # page.  The project itself will be deleted through the project_with_file
            # fixture code.  However, if we don't also make the project private, then
            # there will be an entry on the Collection Discover page with a dead link.
            osf_api.update_node_public_attribute(
                session, project_with_file.id, status=False
            )
