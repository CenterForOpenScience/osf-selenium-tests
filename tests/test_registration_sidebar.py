import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import markers
import utils
from api import osf_api
from pages.registries import (
    RegistrationAnalyticsPage,
    RegistrationCommentsPage,
    RegistrationComponentsPage,
    RegistrationDetailPage,
    RegistrationFilesListPage,
    RegistrationLinksPage,
    RegistrationMetadataPage,
    RegistrationResourcesPage,
    RegistrationWikiPage,
)


@markers.smoke_test
@markers.core_functionality
class TestSubmittedRegistrationSideNavigation:
    """Test all of the links on the side navigation bar of a submitted registration and
    verify the correct registration page is loaded.
    """

    @pytest.fixture()
    def registration_page(self, driver, session):
        """Use OSF api to get the most recent submitted and approved registration and
        navigate to its overview page.
        """
        registration_guid = osf_api.get_most_recent_registration_node_id(session)
        registration_page = RegistrationDetailPage(driver, guid=registration_guid)
        registration_page.goto()
        return registration_page

    def test_metadata_link(self, driver, registration_page):
        registration_page.side_navbar.metadata_link.click()
        assert RegistrationMetadataPage(driver, verify=True)

    def test_files_link(self, driver, registration_page):
        registration_page.side_navbar.files_link.click()
        assert RegistrationFilesListPage(driver, verify=True)

    def test_resources_link(self, driver, registration_page):
        registration_page.side_navbar.resources_link.click()
        assert RegistrationResourcesPage(driver, verify=True)

    def test_wiki_link(self, driver, registration_page):
        registration_page.side_navbar.wiki_link.click()
        assert RegistrationWikiPage(driver, verify=True)

    def test_components_link(self, driver, registration_page):
        registration_page.side_navbar.components_link.click()
        assert RegistrationComponentsPage(driver, verify=True)

    def test_links_link(self, driver, registration_page):
        registration_page.side_navbar.links_link.click()
        assert RegistrationLinksPage(driver, verify=True)

    def test_analytics_link(self, driver, registration_page):
        registration_page.side_navbar.analytics_link.click()
        assert RegistrationAnalyticsPage(driver, verify=True)

    def test_comments_link(self, driver, registration_page):
        registration_page.side_navbar.comments_link.click()
        assert RegistrationCommentsPage(driver, verify=True)

    def test_overview_link(self, driver, session):
        """This test starts on the Registration Metadata page and then clicks the
        Overview link to navigate to the Registration Overview page.
        """
        registration_guid = osf_api.get_most_recent_registration_node_id(session)
        metadata_page = RegistrationMetadataPage(driver, guid=registration_guid)
        metadata_page.goto()
        metadata_page.side_navbar.overview_link.click()
        assert RegistrationDetailPage(driver, verify=True)


@pytest.mark.usefixtures('must_be_logged_in_as_registration_user')
@markers.dont_run_on_prod
@markers.core_functionality
class TestRegistrationOutputs:
    @pytest.fixture()
    def registration_guid(self, session):
        registration_guid = osf_api.get_registration_by_title(
            'Selenium Registration For Outputs Testing'
        )
        return registration_guid

    @pytest.fixture()
    def registration_details_page(self, driver, registration_guid):
        registration_details_page = RegistrationDetailPage(
            driver, guid=registration_guid
        )
        registration_details_page.goto()
        return registration_details_page

    @pytest.fixture()
    def registration_details_page_with_resource(
        self, driver, registration_guid, resource_type
    ):
        registration_details_page = RegistrationDetailPage(
            driver, guid=registration_guid
        )
        osf_api.create_registration_resource(registration_guid, resource_type)
        registration_details_page.goto()
        return registration_details_page

    def create_new_resource(
        self, registration_guid, registration_details_page, resource_type
    ):
        """This method creates new resource of the type given for the given registration"""
        doi = '10.17605'
        registration_details_page.add_resource_button.click()
        registration_details_page.doi_input_field.clear()
        registration_details_page.doi_input_field.click()
        registration_details_page.doi_input_field.send_keys(doi)

        # Select given 'resource_type' from the resource type listbox
        registration_details_page.resource_type_dropdown.click()

        registration_details_page.select_from_dropdown_listbox(resource_type)
        registration_details_page.preview_button.click()
        registration_details_page.resource_type_add_button.click()

    resource_types = ['Data', 'Analytic Code', 'Materials', 'Papers', 'Supplements']

    @pytest.mark.parametrize('resource_type', resource_types)
    def test_add_new_resource(
        self, driver, registration_details_page, registration_guid, resource_type
    ):
        """This test verifies adding new Data output resource for a registration
        and verifies that the Data icon color changes when resource is added"""
        registration_details_page.open_practice_resource_data.click()
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-test-add-resource-section]')
            )
        )
        # Verify and delete the resource if already exists
        resource_id = osf_api.get_registration_resource_id(
            registration_id=registration_guid, resource_type=resource_type
        )
        if resource_id is not None:
            osf_api.delete_registration_resource(registration_guid, resource_type)
            registration_details_page.reload()
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, '[data-test-resource-card-type]')
                )
            )
        self.create_new_resource(
            self, registration_details_page, resource_type=resource_type
        )

        data_resource = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, f'//li/p[text()="{resource_type}"]')
            )
        )
        assert data_resource is not None
        osf_api.delete_registration_resource(registration_guid, resource_type)

    @pytest.mark.parametrize('resource_type', resource_types)
    def test_edit_resource(
        self,
        driver,
        registration_details_page_with_resource,
        registration_guid,
        resource_type,
        fake,
    ):
        """This test updates the description of data output resource for a given registration"""
        resource_description = fake.sentence(nb_words=1)
        registration_details_page_with_resource.open_practice_resource_data.click()

        registration_details_page_with_resource.resource_type_edit_button.click()
        registration_details_page_with_resource.resource_description.click()
        registration_details_page_with_resource.resource_description.clear()
        registration_details_page_with_resource.resource_description.send_keys(
            resource_description
        )
        registration_details_page_with_resource.save_button.click()
        assert (
            utils.clean_text(
                registration_details_page_with_resource.resource_card_description.text
            )
            == resource_description
        )
        osf_api.delete_registration_resource(registration_guid, resource_type)

    @pytest.mark.parametrize('resource_type', resource_types)
    def test_delete_resource(
        self,
        driver,
        registration_details_page_with_resource,
        registration_guid,
        resource_type,
        fake,
    ):
        """This test verifies delete functionality of data output resource for a registration"""

        registration_details_page_with_resource.open_practice_resource_data.click()
        registration_details_page_with_resource.resource_type_delete_button.click()
        registration_details_page_with_resource.resource_type_delete_confirm.click()

        registration_details_page_with_resource.reload()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-test-add-resource-section]')
            )
        )

        assert (
            utils.clean_text(registration_details_page_with_resource.resource_list.text)
            == 'This registration has no resources.'
        )
