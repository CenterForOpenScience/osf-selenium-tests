import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import markers
import settings
from api import osf_api
from pages.collections import (
    CollectionDiscoverPage,
    CollectionModerationAcceptedPage,
    CollectionModerationPendingPage,
    CollectionModerationRejectedPage,
    CollectionModerationRemovedPage,
    CollectionSubmitPage,
)
from pages.login import (
    logout,
    safe_login,
)
from pages.project import ProjectPage


@markers.smoke_test
@markers.core_functionality
class TestCollectionDiscoverPages:
    """This test will load the Discover page for each Collection Provider that exists in
    an environment.
    """

    def providers():
        """Return collection providers to be used in Discover page test. The list of
        collections in some environments (i.e. Staging2) has gotten very long, so a way
        to narrow the list is to set allow_submssions to False in the admin app and we
        can then skip those old testing collections."""
        all_prov = osf_api.get_providers_list(type='collections')
        return [prov for prov in all_prov if prov['attributes']['allow_submissions']]

    @pytest.fixture(params=providers(), ids=[prov['id'] for prov in providers()])
    def provider(self, request):
        return request.param

    def test_discover_page(self, session, driver, provider):
        discover_page = CollectionDiscoverPage(driver, provider=provider)
        discover_page.goto()
        discover_page.loading_indicator.here_then_gone()
        assert CollectionDiscoverPage(driver, verify=True)


@markers.dont_run_on_prod
@markers.core_functionality
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
            # Select the dummy project from the listbox in the Select a project section
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
            WebDriverWait(driver, 5).until(
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
            # After submitting we will end up on the Project page - verify this and
            # verify there is a new section on Project page indicating the project has
            # been submitted to the collection.
            project_page = ProjectPage(driver, verify=True, guid=project_with_file.id)
            assert project_page.collections_container.present()
            assert (
                'Pending entry into Selenium Testing Collection'
                in project_page.pending_collection_display.text
            )
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


@markers.dont_run_on_prod
class TestCollectionModeration:
    @pytest.fixture
    def collection_project(self):
        """Returns a public project using the login session of User Two."""
        session_user_two = osf_api.get_user_two_session()
        project = osf_api.create_project(
            session_user_two,
            title='OSF Collection Project',
            description='Project created using the OSF api for use with selenium testing',
            public=True,
        )
        yield project
        project.delete()

    def update_project_node_with_license(self, session, collection_id, node_id):
        """Helper function that uses the OSF api to update a given project node with a
        valid license value."""

        # Get the license id for the 'CC0 1.0 Universal' license
        license_data = osf_api.get_license_data_for_provider(
            session,
            provider_type='collections',
            provider_id=collection_id,
            license_name='CC0 1.0 Universal',
        )
        license_id = license_data[0]

        # Update the project with the license id
        osf_api.update_node_license(session, node_id, license_id)

    def test_pre_moderation_collection_accept(
        self, session, driver, must_be_logged_in, collection_project
    ):
        """Test the acceptance of a project submission to a public branded collection
        with a pre-moderation workflow.  In this test a project is submitted to a
        collection and a collection moderator must 'accept' the submission before the
        project is included in the collection.  NOTE: In this test case User One is
        used to login to OSF and must therefore be setup through the admin app as a
        moderator or admin for the collection provider being used.  The test will use
        the OSF api to create a submitted project using the session credentials of User
        Two so that the project submitter and moderator are different users.
        """

        session_user_two = osf_api.get_user_two_session()

        # Update the project to set a valid license value
        self.update_project_node_with_license(
            session_user_two, 'selenium', collection_project.id
        )

        # Get data for the Selenium Collection
        collection_provider = osf_api.get_provider(
            session_user_two, type='collections', provider_id='selenium'
        )
        collection_guid = collection_provider['relationships']['primary_collection'][
            'data'
        ]['id']

        # Use the OSF api to submit the test project to the Selenium Collection
        osf_api.submit_project_to_collection(
            session_user_two, collection_guid, collection_project.id
        )

        # Navigate to the Collections Moderation Pending Page. NOTE: User must be a
        # Moderator or Admin for the collection.
        pending_page = CollectionModerationPendingPage(
            driver, provider=collection_provider
        )
        pending_page.goto()
        assert CollectionModerationPendingPage(driver, verify=True)
        pending_page.loading_indicator.here_then_gone()

        # Get the card for the project that was just submitted to the collection
        submisison_card = pending_page.get_submission_card(collection_project.id)

        # Click the Make Decision button on the submission card to reveal the Moderation
        # Dropdown
        submisison_card.find_element_by_css_selector(
            '[data-test-moderation-dropdown-button]'
        ).click()

        # On the Moderation Dropdown, click the Accept Request radio button and enter a
        # comment and then click the Submit button
        pending_page.accept_radio_button.click()
        pending_page.moderation_comment.click()
        pending_page.moderation_comment.send_keys_deliberately(
            'Accepting collection submission via selenium automated test.'
        )
        pending_page.scroll_into_view(pending_page.submit_button.element)
        pending_page.submit_button.click()
        pending_page.loading_indicator.here_then_gone()

        # Navigate to the Accepted Page
        accepted_page = CollectionModerationAcceptedPage(
            driver, provider=collection_provider
        )
        accepted_page.goto()
        assert CollectionModerationAcceptedPage(driver, verify=True)
        accepted_page.loading_indicator.here_then_gone()

        # Find the card for the project that was just accepted and click the link for
        # this project to go to the Project Overview Page. It should be the first one
        # in the table since the default sort order is by Date (newest first).
        accepted_card = accepted_page.get_submission_card(collection_project.id)
        accepted_card.find_element_by_css_selector(
            '[data-test-submission-card-title]'
        ).click()

        # On the Project Overview Page, verify that the Collection Container indicates
        # that the project has been included in the collection.
        project_page = ProjectPage(driver, verify=True)
        assert project_page.collections_container.present()
        assert (
            "Included in Selenium Testing Collection's Collection"
            in project_page.pending_collection_display.text
        )

    def test_pre_moderation_collection_reject(
        self, session, driver, must_be_logged_in, collection_project
    ):
        """Test the rejection of a project submission to a public branded collection
        with a pre-moderation workflow.  In this test a project is submitted to a
        collection and a collection moderator will 'reject' the submission and the
        project is not included in the collection.  NOTE: In this test case User One is
        used to login to OSF and must therefore be setup through the admin app as a
        moderator or admin for the collection provider being used.  The test will use
        the OSF api to create a submitted project using the session credentials of User
        Two so that the project submitter and moderator are different users.
        """

        session_user_two = osf_api.get_user_two_session()

        # Update the project to set a valid license value
        self.update_project_node_with_license(
            session_user_two, 'selenium', collection_project.id
        )

        # Get data for the Selenium Collection
        collection_provider = osf_api.get_provider(
            session_user_two, type='collections', provider_id='selenium'
        )
        collection_guid = collection_provider['relationships']['primary_collection'][
            'data'
        ]['id']

        # Use the OSF api to submit the test project to the Selenium Collection
        osf_api.submit_project_to_collection(
            session_user_two, collection_guid, collection_project.id
        )

        # Navigate to the Collections Moderation Pending Page. NOTE: User must be a
        # Moderator or Admin for the collection.
        pending_page = CollectionModerationPendingPage(
            driver, provider=collection_provider
        )
        pending_page.goto()
        assert CollectionModerationPendingPage(driver, verify=True)
        pending_page.loading_indicator.here_then_gone()

        # Get the card for the project that was just submitted to the collection
        submisison_card = pending_page.get_submission_card(collection_project.id)

        # Click the Make Decision button on the submission card to reveal the Moderation
        # Dropdown
        submisison_card.find_element_by_css_selector(
            '[data-test-moderation-dropdown-button]'
        ).click()

        # On the Moderation Dropdown, click the Reject Request radio button and enter a
        # comment and then click the Submit button
        pending_page.reject_radio_button.click()
        pending_page.moderation_comment.click()
        pending_page.moderation_comment.send_keys_deliberately(
            'Rejecting collection submission via selenium automated test.'
        )
        pending_page.scroll_into_view(pending_page.submit_button.element)
        pending_page.submit_button.click()
        pending_page.loading_indicator.here_then_gone()

        # Navigate to the Rejected Page
        rejected_page = CollectionModerationRejectedPage(
            driver, provider=collection_provider
        )
        rejected_page.goto()
        assert CollectionModerationRejectedPage(driver, verify=True)
        rejected_page.loading_indicator.here_then_gone()

        # Find the card for the project that was just rejected and click the link for
        # this project to go to the Project Overview Page. It should be the first one
        # in the table since the default sort order is by Date (newest first).
        rejected_card = rejected_page.get_submission_card(collection_project.id)
        assert (
            rejected_card.find_element_by_css_selector(
                '[data-test-review-action-comment]'
            ).text
            == '— Rejecting collection submission via selenium automated test.'
        )
        rejected_card.find_element_by_css_selector(
            '[data-test-submission-card-title]'
        ).click()

        # On the Project Overview Page, verify that the Collection Container is absent
        # since the project is NOT included in the collection.
        project_page = ProjectPage(driver, verify=True)
        assert project_page.collections_container.absent()

        # Logout and then login as User Two
        logout(driver)
        safe_login(driver, user=settings.USER_TWO, password=settings.USER_TWO_PASSWORD)

        # Navigate to the Project Overview page for the project that was just remjected
        # from the collection and verify that the user that created and submitted the
        # project can see the reason that it was rejected.
        project_page = ProjectPage(driver, guid=collection_project.id)
        project_page.goto()
        assert project_page.collections_container.present()
        project_page.collections_container.click()
        project_page.collection_justification_link.click()
        assert (
            project_page.collection_justification_reason.text
            == 'Rejecting collection submission via selenium automated test.'
        )
        logout(driver)

    def test_post_moderation_collection_remove(
        self, session, driver, log_in_if_not_already, collection_project
    ):
        """Test the removal of a project from a public branded collection with a
        post-moderation workflow.  In this test a project is submitted to a collection
        via the OSF api, and since it is a post-moderation collection the project is
        automatically accepted as part of the collection.  The collection moderator will
        then 'remove' the submitted project from the collection.  NOTE: In this test case
        User One is used to login to OSF and must therefore be setup through the admin
        app as a moderator or admin for the collection provider being used.  The test
        will use the OSF api to create a submitted project using the session credentials
        of User Two so that the project submitter and moderator are different users.
        """

        session_user_two = osf_api.get_user_two_session()

        # Update the project to set a valid license value
        self.update_project_node_with_license(
            session_user_two, 'selpostmod', collection_project.id
        )

        # Get data for the Selenium Post Moderation Collection
        collection_provider = osf_api.get_provider(
            session_user_two, type='collections', provider_id='selpostmod'
        )
        collection_guid = collection_provider['relationships']['primary_collection'][
            'data'
        ]['id']

        # Use the OSF api to submit the test project to the Selenium Post Moderation
        # Collection
        osf_api.submit_project_to_collection(
            session_user_two, collection_guid, collection_project.id
        )

        # Navigate to the Collections Moderation Accepted Page. NOTE: User must be a
        # Moderator or Admin for the collection.
        accepted_page = CollectionModerationAcceptedPage(
            driver, provider=collection_provider
        )
        accepted_page.goto()
        assert CollectionModerationAcceptedPage(driver, verify=True)
        accepted_page.loading_indicator.here_then_gone()

        # Get the card for the project that was just submitted to the collection
        submisison_card = accepted_page.get_submission_card(collection_project.id)

        # Click the Make Decision button on the submission card to reveal the Moderation
        # Dropdown
        submisison_card.find_element_by_css_selector(
            '[data-test-moderation-dropdown-button]'
        ).click()

        # On the Moderation Dropdown, click the Remove Item radio button and enter a
        # comment and then click the Submit button
        accepted_page.remove_radio_button.click()
        accepted_page.moderation_comment.click()
        accepted_page.moderation_comment.send_keys_deliberately(
            'Removing collection submission via selenium automated test.'
        )
        accepted_page.scroll_into_view(accepted_page.submit_button.element)
        accepted_page.submit_button.click()
        accepted_page.loading_indicator.here_then_gone()

        # Navigate to the Removed Page
        removed_page = CollectionModerationRemovedPage(
            driver, provider=collection_provider
        )
        removed_page.goto()
        assert CollectionModerationRemovedPage(driver, verify=True)
        removed_page.loading_indicator.here_then_gone()

        # Find the card for the project that was just removed and click the link for
        # this project to go to the Project Overview Page. It should be the first one
        # in the table since the default sort order is by Date (newest first).
        removed_card = removed_page.get_submission_card(collection_project.id)
        assert (
            removed_card.find_element_by_css_selector(
                '[data-test-review-action-comment]'
            ).text
            == '— Removing collection submission via selenium automated test.'
        )
        removed_card.find_element_by_css_selector(
            '[data-test-submission-card-title]'
        ).click()

        # On the Project Overview Page, verify that the Collection Container is absent
        # since the project is no longer included in the collection.
        project_page = ProjectPage(driver, verify=True)
        assert project_page.collections_container.absent()

        # Logout and then login as User Two
        logout(driver)
        safe_login(driver, user=settings.USER_TWO, password=settings.USER_TWO_PASSWORD)

        # Navigate to the Project Overview page for the project that was just removed
        # from the collection and verify that the user that created and submitted the
        # project can see the reason that it was removed.
        project_page = ProjectPage(driver, guid=collection_project.id)
        project_page.goto()
        assert project_page.collections_container.present()
        project_page.collections_container.click()
        project_page.collection_justification_link.click()
        assert (
            project_page.collection_justification_reason.text
            == 'Removing collection submission via selenium automated test.'
        )
