import pytest
from selenium.webdriver.common.action_chains import ActionChains

import markers
from api import osf_api
from pages.project import RegistrationsPage
from pages.registries import (
    DraftRegistrationMetadataPage,
    DraftRegistrationReviewPage,
)
from pages.support import SupportPage


@pytest.fixture()
def registrations_page(driver, default_project):
    """Fixture that uses a temporary project created in the testing environments and
    then navigates to the Registrations page for that project.
    """
    registrations_page = RegistrationsPage(driver, guid=default_project.id)
    registrations_page.goto()
    return registrations_page


@pytest.fixture()
def registrations_page_with_draft(session, registrations_page):
    """This fixture uses the registrations_page fixture above and adds a draft
    registration to the temporary project.  NOTE: Since we are creating the draft
    registration from a temporary project that gets automatically deleted when we are
    done with it, the draft registration as a child of the project will also get
    deleted.
    """

    # First get the list of allowed registration schemas for OSF in a name and id pair
    # list. Then loop through the list to pull out just the id for the Open-Ended
    # Registration schema. We'll need this schema id to create the draft.
    schema_list = osf_api.get_registration_schemas_for_provider(
        provider_id='osf', data_type='name_id'
    )
    for schema in schema_list:
        if schema[0] == 'Open-Ended Registration':
            schema_id = schema[1]
    # Use the api to create a draft registration for the temporary project
    osf_api.create_draft_registration(
        session, node_id=registrations_page.guid, schema_id=schema_id
    )
    # Reload the page so that the draft is visible on the tab
    registrations_page.reload()
    registrations_page.draft_registrations_tab.click()
    return registrations_page


@markers.dont_run_on_prod
@pytest.mark.usefixtures('must_be_logged_in')
class TestProjectRegistrationsPage:
    def test_empty_registrations_tab(self, driver, registrations_page):
        """Tests that when the Project Registration page is first loaded, the submitted
        Registrations tab is selected and displayed by default. Also since this is a
        newly created project there should not be any existing submitted registrations.
        """
        assert (
            registrations_page.registrations_tab.get_attribute('aria-selected')
            == 'true'
        )
        assert (
            registrations_page.draft_registrations_tab.get_attribute('aria-selected')
            == 'false'
        )
        assert registrations_page.registration_card.absent()
        assert (
            registrations_page.no_registrations_message_1.text
            == 'There have been no completed registrations of this project.'
        )
        assert (
            registrations_page.no_registrations_message_2.text
            == 'Start a new registration by clicking the “New registration” button. Once created, registrations cannot be edited or deleted.'
        )
        assert (
            registrations_page.no_registrations_message_3.text
            == 'Learn more about registrations here.'
        )
        # Click 'here' link and verify redirection to support page
        registrations_page.here_support_link.click()
        assert SupportPage(driver, verify=True)

    def test_empty_draft_registrations_tab(self, driver, registrations_page):
        """Tests that when the Project Registration page is first loaded, you can switch
        to the Draft Registrations tab by clicking the tab link.  And since this is a
        newly created project there should not be any existing draft registrations.
        """
        registrations_page.draft_registrations_tab.click()
        assert (
            registrations_page.registrations_tab.get_attribute('aria-selected')
            == 'false'
        )
        assert (
            registrations_page.draft_registrations_tab.get_attribute('aria-selected')
            == 'true'
        )
        assert registrations_page.draft_registration_card.absent()
        assert (
            registrations_page.no_draft_registrations_message_1.text
            == 'There are no draft registrations of this project.'
        )
        assert (
            registrations_page.no_draft_registrations_message_2.text
            == 'Start a new registration by clicking the “New registration” button. Once created, registrations cannot be edited or deleted.'
        )
        assert (
            registrations_page.no_draft_registrations_message_3.text
            == 'Learn more about registrations here.'
        )
        # Click 'here' link and verify redirection to support page
        registrations_page.here_support_link.click()
        assert SupportPage(driver, verify=True)

    def test_create_new_registration_modal(self, driver, registrations_page):
        """Tests the Create Registration Modal window that opens when you click the
        New registration button on the Project Registrations page.
        """
        registrations_page.new_registration_button.click()
        create_registration_modal = registrations_page.create_registration_modal
        assert create_registration_modal.modal_window.present()
        # Verify that the first schema in the list is pre-selected
        first_schema = create_registration_modal.schema_list[0]
        assert first_schema.find_element_by_css_selector('.ember-view').is_selected()
        # Get list of allowed schemas for OSF Registries from the api and verify the
        # list on the modal matches the api list
        api_schema_list = osf_api.get_registration_schemas_for_provider(
            provider_id='osf', data_type='name'
        )
        api_schema_list.sort()
        modal_schema_list = create_registration_modal.get_schema_names_list()
        modal_schema_list.sort()
        assert api_schema_list == modal_schema_list
        # Click the Cancel button to close the modal window
        try:
            create_registration_modal.cancel_button.click()
        except ValueError:
            # In some environments there may be several schemas listed on the modal
            # which may push the Cancel button below the visible part of the screen
            # depending on the screen resolution. Currently this modal window does
            # not have the ability to vertically scroll, so the scroll_into_view
            # method will not work. There is an open ticket for the scrolling issue:
            # ENG-3740.
            cancel_button = driver.find_element_by_css_selector(
                'button[data-test-new-registration-modal-cancel-button]'
            )
            ActionChains(driver).move_to_element(cancel_button).perform()
            cancel_button.click()
        # Verify the modal window has closed
        assert create_registration_modal.modal_window.absent()

    def test_create_new_draft_registration(self, driver, registrations_page):
        """Tests the creation of a new draft registration from the Project Registrations
        page by clicking the New regsitration button on the page.  Then on the Create
        Registration modal window, select a schema and click the Create draft button to
        actually create the draft registration.
        """
        registrations_page.new_registration_button.click()
        create_registration_modal = registrations_page.create_registration_modal
        assert create_registration_modal.modal_window.present()
        create_registration_modal.select_schema_radio_button(
            schema_name='Open-Ended Registration'
        )
        try:
            create_registration_modal.create_draft_button.click()
        except ValueError:
            # In some environments there may be several schemas listed on the modal
            # which may push the Create draft button below the visible part of the
            # screen depending on the screen resolution. Currently this modal window
            # does not have the ability to vertically scroll, so the scroll_into_view
            # method will not work. There is an open ticket for the scrolling issue:
            # ENG-3740.
            create_draft_button = driver.find_element_by_css_selector(
                'button[data-test-new-registration-modal-create-draft-button]'
            )
            ActionChains(driver).move_to_element(create_draft_button).perform()
            create_draft_button.click()
        # Verify that you are redirected to the Draft Registration Metadata page
        DraftRegistrationMetadataPage(driver, verify=True)

    def test_review_draft_registration(
        self, session, driver, registrations_page_with_draft
    ):
        """Using the registrations_page_with_draft fixture that already has a draft
        registration created for the temporary project, verify that the draft
        registration is visble on the Draft registrations tab of the Project
        Registrations page.  Then click the Review button and verify that you are
        redirected to the Draft Registration Review page.
        """
        assert registrations_page_with_draft.draft_registration_card.present()
        assert (
            registrations_page_with_draft.draft_registration_title.text
            == 'OSF Test Project'
        )
        assert (
            registrations_page_with_draft.draft_registration_schema_name.text
            == 'Open-Ended Registration'
        )
        assert (
            registrations_page_with_draft.draft_registration_provider.text
            == 'OSF Registries'
        )
        registrations_page_with_draft.review_draft_button.click()
        assert DraftRegistrationReviewPage(driver, verify=True)

    def test_edit_draft_registration(
        self, session, driver, registrations_page_with_draft
    ):
        """Using the registrations_page_with_draft fixture that already has a draft
        registration created for the temporary project, verify that the draft
        registration is visble on the Draft registrations tab of the Project
        Registrations page.  Then click the Edit button and verify that you are
        redirected to the Draft Registration Metadata page.
        """
        assert registrations_page_with_draft.draft_registration_card.present()
        assert (
            registrations_page_with_draft.draft_registration_title.text
            == 'OSF Test Project'
        )
        registrations_page_with_draft.edit_draft_button.click()
        DraftRegistrationMetadataPage(driver, verify=True)

    def test_delete_draft_registration(
        self, session, driver, registrations_page_with_draft
    ):
        """Using the registrations_page_with_draft fixture that already has a draft
        registration created for the temporary project, verify that the draft
        registration is visble on the Draft registrations tab of the Project
        Registrations page.  Then verify that you can delete the draft registration
        using the Delete button on the page.
        """
        assert registrations_page_with_draft.draft_registration_card.present()
        assert (
            registrations_page_with_draft.draft_registration_title.text
            == 'OSF Test Project'
        )
        # Click the Delete button for the Draft Registration card and then click the
        # Delete button on the Comfirm Delete Draft Registration Modal
        registrations_page_with_draft.delete_draft_button.click()
        registrations_page_with_draft.delete_draft_registration_modal.delete_button.click()
        # Verify that the Draft Registration is no longer visible on the Draft
        # Registrations tab.
        assert registrations_page_with_draft.draft_registration_card.absent()
        assert (
            registrations_page_with_draft.no_draft_registrations_message_1.text
            == 'There are no draft registrations of this project.'
        )
