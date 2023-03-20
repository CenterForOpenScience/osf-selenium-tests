import pytest

import markers
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
