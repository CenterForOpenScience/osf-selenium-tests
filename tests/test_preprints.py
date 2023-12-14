import logging
import os
import re
from datetime import datetime

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

import markers
import settings
from api import osf_api
from pages.login import logout
from pages.preprints import (
    BrandedPreprintsDiscoverPage,
    PendingPreprintDetailPage,
    PreprintDetailPage,
    PreprintDiscoverPage,
    PreprintEditPage,
    PreprintLandingPage,
    PreprintPageNotFoundPage,
    PreprintSubmitPage,
    PreprintWithdrawPage,
    ReviewsDashboardPage,
    ReviewsSubmissionsPage,
    ReviewsWithdrawalsPage,
)
from utils import (
    close_current_tab,
    find_current_browser,
    switch_to_new_tab,
)


logger = logging.getLogger(__name__)


@pytest.fixture
def landing_page(driver):
    landing_page = PreprintLandingPage(driver)
    landing_page.goto()
    return landing_page


# TODO: Add checking for missing translations
@pytest.mark.usefixtures('must_be_logged_in')
class TestPreprintWorkflow:
    @markers.dont_run_on_prod
    @pytest.mark.usefixtures('delete_user_projects_at_setup')
    def test_create_preprint_from_landing(
        self, session, driver, landing_page, project_with_file
    ):
        supplemental_guid = None
        try:
            landing_page = PreprintLandingPage(driver, verify=True)
            # Create a date and time stamp before starting the creation of the preprint.
            # This may be used later to find the guid for the preprint.
            now = datetime.utcnow()
            date_time_stamp = now.strftime('%Y-%m-%dT%H:%M:%S')
            # need to figure why this locator needs to be added manually
            landing_page.add_preprint_button = driver.find_element_by_css_selector(
                '[data-analytics-name="Add a preprint"]'
            )
            landing_page.add_preprint_button.click()
            submit_page = PreprintSubmitPage(driver, verify=True)

            # Wait for select a service to show
            WebDriverWait(driver, 10).until(
                EC.visibility_of(submit_page.select_a_service_help_text)
            )
            submit_page.select_a_service_save_button.click()
            submit_page.upload_from_existing_project_button.click()
            submit_page.upload_project_selector.click()
            submit_page.upload_project_help_text.here_then_gone()
            submit_page.upload_project_selector_project.click()

            submit_page.upload_select_file.click()
            submit_page.upload_file_save_continue.click()

            # Author Assertions section
            # Note: We can't use the submit_page.save_author_assertions object here,
            # because it is disabled and any time we use an object defined in
            # pages/preprints.py it uses get_web_element() in the Locator class.
            # Within get_web_element() the element_to_be_clickable method is used,
            # and this method will always fail for disabled objects.  So in this
            # instance we have to get the button object using the driver.find_element
            # method while it is disabled.  After the button becomes enabled (i.e.
            # after required data has been provided) then we can use the
            # submit_page.save_author_assertions object to check the disabled
            # property.  See implementation below.
            assert driver.find_element(
                By.CSS_SELECTOR, '[data-test-author-assertions-continue]'
            ).get_property('disabled')
            assert submit_page.public_data_input.absent()
            submit_page.public_available_button.click()
            assert submit_page.public_data_input.present()
            submit_page.public_data_input.click()
            submit_page.public_data_input.send_keys_deliberately('https://osf.io/')
            # Need to scroll down since the Preregistration radio buttons are obscured
            # by the Dev mode warning in test environments
            submit_page.scroll_into_view(submit_page.preregistration_no_button.element)
            assert submit_page.preregistration_input.absent()
            submit_page.preregistration_no_button.click()
            assert submit_page.preregistration_input.present()
            submit_page.preregistration_input.click()
            submit_page.preregistration_input.send_keys_deliberately('QA Testing')
            # Save button is now enabled so we can use the object as defined in
            # pages/preprints.py
            assert submit_page.save_author_assertions.is_enabled()
            submit_page.save_author_assertions.click()

            submit_page.basics_license_dropdown.click()
            # The order of the options in the license dropdown is not consistent across
            # test environments. So we have to select by the actual text value instead
            # of by relative position (i.e. 3rd option in listbox).
            license_select = Select(submit_page.basics_license_dropdown)
            license_select.select_by_visible_text('CC0 1.0 Universal')
            # Need to scroll down since the Keyword/tags section is obscured by the Dev
            # mode warning in the test environments
            submit_page.scroll_into_view(submit_page.basics_tags_section.element)
            submit_page.basics_tags_section.click()
            submit_page.basics_tags_input.send_keys('selenium\r')
            submit_page.basics_abstract_input.click()
            submit_page.basics_abstract_input.send_keys('Center for Open Selenium')
            submit_page.basics_save_button.click()

            # Wait for discipline help text
            submit_page.first_discipline.click()
            submit_page.discipline_save_button.click()

            # Wait for authors box to show
            submit_page.authors_save_button.click()

            # Conflict of Interest section:
            assert driver.find_element(
                By.CSS_SELECTOR, '[data-test-coi-continue]'
            ).get_property('disabled')
            assert submit_page.no_coi_text_box.absent()
            submit_page.conflict_of_interest_no.click()
            assert submit_page.no_coi_text_box.present()
            assert submit_page.coi_save_button.is_enabled()
            submit_page.coi_save_button.click()

            # Wait for Supplemental materials to show
            submit_page.supplemental_create_new_project.click()
            submit_page.supplemental_save_button.click()

            submit_page.create_preprint_button.click()
            submit_page.modal_create_preprint_button.click()

            preprint_detail = PendingPreprintDetailPage(driver, verify=True)
            WebDriverWait(driver, 10).until(EC.visibility_of(preprint_detail.title))

            assert preprint_detail.title.text == project_with_file.title
            # Capture guid of supplemental materials project created during workflow
            match = re.search(
                r'Supplemental Materials\s+([a-z0-9]{4,8})\.osf\.io/([a-z0-9]{5})',
                preprint_detail.view_page.text,
            )
            assert match is not None
            supplemental_guid = match.group(2)

        finally:
            # If there was an error above and we did not capture the guid for the
            # supplemental materials project, then we need to get it if it exists.
            if supplemental_guid is None:
                # Get the list of preprints for the current user
                preprints = osf_api.get_preprints_list_for_user(session)
                for preprint in preprints:
                    # Go through the list of preprints and if any of them has a creation
                    # date and time after the date time stamp that we created before
                    # starting this preprint then that is our preprint, so use its guid
                    # to get the guid for the supplemental materials project.
                    if preprint['attributes']['date_created'] > date_time_stamp:
                        supplemental_guid = (
                            osf_api.get_preprint_supplemental_material_guid(
                                session, preprint['id']
                            )
                        )
                        break

            # We need to always delete the supplemental materials project if it exists
            if supplemental_guid is not None:
                osf_api.delete_project(session, supplemental_guid, None)

            # If we are still stuck on the Preprint Submit page then refresh it to see
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

    @pytest.fixture
    def preprint_detail_page(self, driver, session):
        """Fixture that uses the OSF api to create a published preprint in OSF
        Preprints and then navigates to the Preprint Detail page for this preprint.
        """
        preprint_node = osf_api.create_preprint(
            session,
            provider_id='osf',
            title='OSF Selenium Preprint',
            license_name='CC0 1.0 Universal',
            subject_name='Engineering',
        )
        preprint_detail_page = PreprintDetailPage(driver, guid=preprint_node)
        preprint_detail_page.goto()
        return preprint_detail_page

    @markers.dont_run_on_prod
    def test_edit_preprint(self, session, driver, preprint_detail_page):
        """Test the Edit Preprint functionality. Using the preprint_detail_page fixture
        we start on the Preprint Detail page for an api created preprint. Then click
        the 'Edit preprint' button to go to the Edit Preprint page. Make some minor
        updates to the preprint and save. Lastly verify that the edits that were made
        are displayed correctly on the Preprint Detail page.
        """
        assert PreprintDetailPage(driver, verify=True)
        preprint_detail_page.edit_preprint_button.click()
        edit_page = PreprintEditPage(driver, verify=True)
        # Click the Basics section to reveal the Basic form fields
        edit_page.scroll_into_view(edit_page.basics_section.element)
        edit_page.basics_section.click()
        # Add another Tag and click the Save and continue button
        edit_page.basics_tags_section.click()
        edit_page.basics_tags_input.send_keys(os.environ['PYTEST_CURRENT_TEST'])
        edit_page.basics_tags_input.send_keys('\r')
        edit_page.basics_save_button.click()
        # Next add another subject in the Discipline section
        edit_page.scroll_into_view(edit_page.discipline_section.element)
        edit_page.discipline_section.click()
        # Need to wait a couple seconds for the event code behind the Subjects listbox
        # to be operable, so wait for the Changes saved message in the Basics section
        # to disappear.
        edit_page.basics_section_changes_saved_indicator.here_then_gone()
        edit_page.select_primary_subject_by_name('Business')
        edit_page.scroll_into_view(edit_page.discipline_save_button.element)
        edit_page.discipline_save_button.click()
        # Wait for the Authors section to become visible to give the addition of the
        # subject time to actually save before we leave the page.
        WebDriverWait(driver, 5).until(EC.visibility_of(edit_page.authors_save_button))
        # Click Return to preprint button to go back to Preprint Detail page
        edit_page.scroll_into_view(edit_page.return_to_preprint_button.element)
        edit_page.return_to_preprint_button.click()
        detail_page = PendingPreprintDetailPage(driver, verify=True)
        # Verify new Subject appears on the page
        subjects = detail_page.subjects
        subject_found = False
        for subject in subjects:
            if subject.text == 'Business':
                subject_found = True
                break
        assert subject_found
        # Verify new Tag appears on the page
        tags = detail_page.tags
        tag_found = False
        for tag in tags:
            if tag.text == os.environ['PYTEST_CURRENT_TEST']:
                tag_found = True
                break
        assert tag_found

    @markers.dont_run_on_prod
    def test_withdraw_preprint(self, session, driver, preprint_detail_page):
        """Test the Withdraw Preprint functionality. Using the preprint_detail_page
        fixture we start on the Preprint Detail page for an api created preprint. Then
        click the 'Edit preprint' button to go to the Edit Preprint page. Scroll to the
        bottom of the Edit Preprint page and click the 'Withdraw preprint' button. Next
        on the Withdraw Preprint page enter a reason for withdrawing the preprint and
        click the 'Request withdrawal' button. OSF Preprints is a non-moderated preprint
        provider so the actual withdrawal request is accepted and completed by an admin
        user in the OSF admin app. The best we can do here is to verify through the api
        that the withdrawal request record is created.
        """
        assert PreprintDetailPage(driver, verify=True)
        preprint_detail_page.edit_preprint_button.click()
        edit_page = PreprintEditPage(driver, verify=True)
        edit_page.scroll_into_view(edit_page.withdraw_preprint_button.element)
        edit_page.withdraw_preprint_button.click()
        withdraw_page = PreprintWithdrawPage(driver, verify=True)
        withdraw_page.reason_for_withdrawal_textarea.send_keys_deliberately(
            'OSF Selenium Test: '
        )
        withdraw_page.reason_for_withdrawal_textarea.send_keys(
            os.environ['PYTEST_CURRENT_TEST']
        )
        withdraw_page.request_withdrawal_button.click()
        # Should be redirected back to Preprint Detail page
        assert PendingPreprintDetailPage(driver, verify=True)
        # Verify via the api that the Withdrawal Request record was created
        requests = osf_api.get_preprint_requests_records(
            node_id=preprint_detail_page.guid
        )
        if requests:
            # Look for 'withdrawal' request_type and verify it has a 'pending' status
            record_found = False
            for request in requests:
                if request['attributes']['request_type'] == 'withdrawal':
                    assert request['attributes']['machine_state'] == 'pending'
                    record_found = True
                    break
            if not record_found:
                raise ValueError(
                    'Withdrawal Request record was not found for preprint: `{}`'.format(
                        preprint_detail_page.guid
                    )
                )
        else:
            raise ValueError(
                'No Requests records found for preprint: `{}`'.format(
                    preprint_detail_page.guid
                )
            )


@markers.dont_run_on_prod
class TestPreprintModeration:
    def test_accept_pre_moderated_preprint(self, session, driver, must_be_logged_in):
        """Test the acceptance of a preprint submission to a Preprint Provider with a
        Pre-moderation workflow. In this workflow a preprint is submitted to the
        preprint service provider but is not yet published. A moderator must then
        'accept' the preprint submission before it is published and publicly accessible.
        NOTE: In this test case User One is used to login to OSF and must therefore be
        setup through the admin app as a moderator or admin for the Preprint Provider
        being used.  The test will use the OSF api to create a submitted preprint, but
        the preprint will be submitted using the session credentials of User Two so
        that the preprint submitter and moderator are different users.
        """
        # The following Preprint Provider must be setup in each testing environment.
        provider_id = 'selpremod'
        provider_name = 'Selenium Pre-moderation'
        preprint_title = 'OSF Selenium Pre-moderation Preprint'

        # NOTE: Using User Two to create the preprint through the api so that the user
        # that submits the preprint is different from the user that accepts or rejects
        # it.
        session_user_two = osf_api.get_user_two_session()
        preprint_node = osf_api.create_preprint(
            session_user_two,
            provider_id=provider_id,
            title=preprint_title,
            license_name='CC0 1.0 Universal',
            subject_name='Engineering',
        )
        # Use the api to verify that the Preprint is not yet published and that its
        # review status is 'pending'.
        prep_attr = osf_api.get_preprint_publish_and_review_states(
            preprint_node=preprint_node
        )
        assert not prep_attr[0]
        assert prep_attr[1] == 'pending'
        # Load Reviews Dashboard page first and then click the Submissions link for the
        # Pre-moderation provider to go to that page.
        reviews_dashboard_page = ReviewsDashboardPage(driver)
        reviews_dashboard_page.goto()
        assert ReviewsDashboardPage(driver, verify=True)
        reviews_dashboard_page.loading_indicator.here_then_gone()
        reviews_dashboard_page.click_provider_group_link(provider_name, 'Submissions')
        submissions_page = ReviewsSubmissionsPage(driver, verify=True)
        submissions_page.loading_indicator.here_then_gone()
        # On the Reviews Submissions page, click the row for the preprint that was just
        # submitted above. It should be the first in the list since they are sorted
        # newest to oldest.
        submissions_page.click_submission_row(provider_id, preprint_node)
        preprint_detail_page = PendingPreprintDetailPage(driver, verify=True)
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button.btn.dropdown-toggle.btn-success')
            )
        )
        # Verify that the Preprint has a Pending status in the status bar
        assert preprint_detail_page.status.text == 'pending'
        # Click the Make decision button to reveal the review options. Then click
        # the Accept radio button, enter a reason in the text box and click the
        # Submit decision button to complete the review.
        preprint_detail_page.make_decision_button.click()
        preprint_detail_page.accept_radio_button.click()
        preprint_detail_page.reason_textarea.send_keys_deliberately(
            'Selenium Testing - Accepting Pre-Moderated Preprint'
        )
        preprint_detail_page.submit_decision_button.click()
        # Should end up back on the Reviews Submission page
        assert ReviewsSubmissionsPage(driver, verify=True)
        # Use the api to verify that the Preprint is now published and that its review
        # status is now 'accepted'.
        prep_attr = osf_api.get_preprint_publish_and_review_states(
            preprint_node=preprint_node
        )
        assert prep_attr[0]
        assert prep_attr[1] == 'accepted'
        # Logout and navigate to the Preprint Detail page since it is now public.
        logout(driver)
        preprint_page = PreprintDetailPage(driver, guid=preprint_node)
        preprint_page.goto()
        assert PreprintDetailPage(driver, verify=True)
        WebDriverWait(driver, 5).until(EC.visibility_of(preprint_page.title))
        assert preprint_page.title.text == preprint_title
        assert provider_id in driver.current_url

    def test_reject_pre_moderated_preprint(
        self, session, driver, log_in_if_not_already
    ):
        """Test the rejection of a preprint submission to a Preprint Provider with a
        Pre-moderation workflow. In this workflow a preprint is submitted to the
        preprint service provider but is not yet published. A moderator will then
        'reject' the preprint submission.  The rejected preprint will never become
        published or publicly accessible.
        NOTE: In this test case User One is used to login to OSF and must therefore be
        setup through the admin app as a moderator or admin for the Preprint Provider
        being used.  The test will use the OSF api to create a submitted preprint, but
        the preprint will be submitted using the session credentials of User Two so
        that the preprint submitter and moderator are different users.
        """
        # The following Preprint Provider must be setup in each testing environment.
        provider_id = 'selpremod'
        provider_name = 'Selenium Pre-moderation'
        preprint_title = 'OSF Selenium Pre-moderation Preprint'

        # NOTE: Using User Two to create the preprint through the api so that the user
        # that submits the preprint is different from the user that accepts or rejects
        # it.
        session_user_two = osf_api.get_user_two_session()
        preprint_node = osf_api.create_preprint(
            session_user_two,
            provider_id=provider_id,
            title=preprint_title,
            license_name='CC0 1.0 Universal',
            subject_name='Engineering',
        )
        # Use the api to verify that the Preprint is not yet published and that its
        # review status is 'pending'.
        prep_attr = osf_api.get_preprint_publish_and_review_states(
            preprint_node=preprint_node
        )
        assert not prep_attr[0]
        assert prep_attr[1] == 'pending'
        # Load Reviews Dashboard page first and then click the Submissions link for the
        # Pre-moderation provider to go to that page.
        reviews_dashboard_page = ReviewsDashboardPage(driver)
        reviews_dashboard_page.goto()
        assert ReviewsDashboardPage(driver, verify=True)
        reviews_dashboard_page.loading_indicator.here_then_gone()
        reviews_dashboard_page.click_provider_group_link(provider_name, 'Submissions')
        submissions_page = ReviewsSubmissionsPage(driver, verify=True)
        submissions_page.loading_indicator.here_then_gone()
        # On the Reviews Submissions page, click the row for the preprint that was just
        # submitted above. It should be the first in the list since they are sorted
        # newest to oldest.
        submissions_page.click_submission_row(provider_id, preprint_node)
        preprint_detail_page = PendingPreprintDetailPage(driver, verify=True)
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button.btn.dropdown-toggle.btn-success')
            )
        )
        # Verify that the Preprint has a Pending status in the status bar
        assert preprint_detail_page.status.text == 'pending'
        # Click the Make decision button to reveal the review options. Then click
        # the Reject radio button, enter a reason in the text box and click the
        # Submit decision button to complete the review.
        preprint_detail_page.make_decision_button.click()
        preprint_detail_page.reject_radio_button.click()
        preprint_detail_page.reason_textarea.send_keys_deliberately(
            'Selenium Testing - Rejecting Pre-Moderated Preprint'
        )
        preprint_detail_page.submit_decision_button.click()
        # Should end up back on the Reviews Submission page
        assert ReviewsSubmissionsPage(driver, verify=True)
        # Use the api to verify that the Preprint is still not published and that its
        # review status is now 'rejected'.
        prep_attr = osf_api.get_preprint_publish_and_review_states(
            preprint_node=preprint_node
        )
        assert not prep_attr[0]
        assert prep_attr[1] == 'rejected'
        # Logout and attempt to navigate to the Preprint Detail page. We should get a
        # Page Not Found page since the rejected preprint is not public.
        logout(driver)
        preprint_page = PendingPreprintDetailPage(driver, guid=preprint_node)
        preprint_page.goto(expect_redirect_to=PreprintPageNotFoundPage)
        page_not_found_page = PreprintPageNotFoundPage(driver, verify=True)
        assert page_not_found_page.page_header.text == 'Page not found'

    def test_approve_withdrawal_request_pre_moderated_preprint(
        self, session, driver, log_in_if_not_already
    ):
        """Test the approval of a Withdrawal Request for a preprint submitted and
        accepted by a preprint provider with a Pre-moderation workflow. In this
        workflow the moderator will approve/accept the withdrawal request and the
        public preprint will be replaced with a Withdrawn tombstone page in OSF. The
        test will use the OSF api to create a submitted preprint and to accept the
        preprint and create the withdrawal request record. The actual test steps will
        thus start at the point where the moderator takes action from the Reviews
        Dashboard page to approve the withdrawal request.
        NOTE: In this test case User One is used to login to OSF and must therefore be
        setup through the admin app as a moderator or admin for the Preprint Provider
        being used.
        """
        # The following Preprint Provider must be setup in each testing environment.
        provider_id = 'selpremod'
        provider_name = 'Selenium Pre-moderation'
        preprint_title = 'OSF Selenium Pre-moderation Preprint'

        # NOTE: Using User Two to create the preprint through the api so that the user
        # that submits the preprint is different from the user that accepts or rejects
        # it.
        session_user_two = osf_api.get_user_two_session()
        preprint_node = osf_api.create_preprint(
            session_user_two,
            provider_id=provider_id,
            title=preprint_title,
            license_name='CC0 1.0 Universal',
            subject_name='Engineering',
        )
        # Set session to None before calling accept_preprint so that the api function
        # will use the default User One session which should have the permissions as
        # a moderator to be able to accept the preprint.
        osf_api.accept_moderated_preprint(session=None, preprint_node=preprint_node)
        # Next use the api to create a withdrawal request (using User Two again)
        osf_api.create_preprint_withdrawal_request(
            session=session_user_two, preprint_node=preprint_node
        )
        # Load Reviews Dashboard page first and then click the Submissions link for the
        # Pre-moderation provider to go to that page.
        reviews_dashboard_page = ReviewsDashboardPage(driver)
        reviews_dashboard_page.goto()
        assert ReviewsDashboardPage(driver, verify=True)
        reviews_dashboard_page.loading_indicator.here_then_gone()
        reviews_dashboard_page.click_provider_group_link(provider_name, 'Submissions')
        submissions_page = ReviewsSubmissionsPage(driver, verify=True)
        submissions_page.loading_indicator.here_then_gone()
        # Click the Withdrawal Requests tab
        submissions_page.withdrawal_requests_tab.click()
        withdrawals_page = ReviewsWithdrawalsPage(driver, verify=True)
        withdrawals_page.loading_indicator.here_then_gone()
        # On the Withdrawal Requests page, click the row for the preprint that was just
        # submitted above. It should be the first in the list since they are sorted
        # newest to oldest.
        withdrawals_page.click_requests_row(provider_id, preprint_node)
        preprint_detail_page = PendingPreprintDetailPage(driver, verify=True)
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button.btn.dropdown-toggle.btn-success')
            )
        )
        # Verify that the Preprint has a Pending status in the status bar
        assert preprint_detail_page.status.text == 'pending'
        # Click the Make decision button to reveal the review options. Then click
        # the Approve radio button, enter a reason in the text box and click the
        # Submit decision button to complete the review.
        preprint_detail_page.make_decision_button.click()
        preprint_detail_page.accept_radio_button.click()
        preprint_detail_page.reason_textarea.clear()
        preprint_detail_page.reason_textarea.send_keys_deliberately(
            'Selenium Testing - Approving Withdrawal Request of Pre-Moderated Preprint'
        )
        preprint_detail_page.submit_decision_button.click()
        # Should end up back on the Reviews Submission page
        assert ReviewsSubmissionsPage(driver, verify=True)
        # Use the api to verify that the Preprint is not published and that its review
        # status is now 'withdrawn'.
        prep_attr = osf_api.get_preprint_publish_and_review_states(
            preprint_node=preprint_node
        )
        assert not prep_attr[0]
        assert prep_attr[1] == 'withdrawn'
        # Logout and navigate to the Preprint Detail page. We should see a Withdrawn
        # tombstone page.
        logout(driver)
        preprint_page = PreprintDetailPage(driver, guid=preprint_node)
        preprint_page.goto()
        assert PreprintDetailPage(driver, verify=True)
        WebDriverWait(driver, 5).until(EC.visibility_of(preprint_page.title))
        assert preprint_page.title.text == preprint_title
        assert (
            preprint_page.status_explanation.text == 'This preprint has been withdrawn.'
        )

    def test_decline_withdrawal_request_pre_moderated_preprint(
        self, session, driver, log_in_if_not_already
    ):
        """Test the declining of a Withdrawal Request for a preprint submitted and
        accepted by a preprint provider with a Pre-moderation workflow. In this
        workflow the moderator will decline the withdrawal request and the preprint
        will remain accepted and publicly accessible. The test will use the OSF api
        to create a submitted preprint and to accept the preprint and create the
        withdrawal request record. The actual test steps will thus start at the point
        where the moderator takes action from the Reviews Dashboard page to decline
        the withdrawal request.
        NOTE: In this test case User One is used to login to OSF and must therefore be
        setup through the admin app as a moderator or admin for the Preprint Provider
        being used.
        """
        # The following Preprint Provider must be setup in each testing environment.
        provider_id = 'selpremod'
        provider_name = 'Selenium Pre-moderation'
        preprint_title = 'OSF Selenium Pre-moderation Preprint'

        # NOTE: Using User Two to create the preprint through the api so that the user
        # that submits the preprint is different from the user that accepts or rejects
        # it.
        session_user_two = osf_api.get_user_two_session()
        preprint_node = osf_api.create_preprint(
            session_user_two,
            provider_id=provider_id,
            title=preprint_title,
            license_name='CC0 1.0 Universal',
            subject_name='Engineering',
        )
        # Set session to None before calling accept_preprint so that the api function
        # will use the default User One session which should have the permissions as
        # a moderator to be able to accept the preprint.
        osf_api.accept_moderated_preprint(session=None, preprint_node=preprint_node)
        # Next use the api to create a withdrawal request (using User Two again)
        osf_api.create_preprint_withdrawal_request(
            session=session_user_two, preprint_node=preprint_node
        )
        # Load Reviews Dashboard page first and then click the Submissions link for the
        # Pre-moderation provider to go to that page.
        reviews_dashboard_page = ReviewsDashboardPage(driver)
        reviews_dashboard_page.goto()
        assert ReviewsDashboardPage(driver, verify=True)
        reviews_dashboard_page.loading_indicator.here_then_gone()
        reviews_dashboard_page.click_provider_group_link(provider_name, 'Submissions')
        submissions_page = ReviewsSubmissionsPage(driver, verify=True)
        submissions_page.loading_indicator.here_then_gone()
        # Click the Withdrawal Requests tab
        submissions_page.withdrawal_requests_tab.click()
        withdrawals_page = ReviewsWithdrawalsPage(driver, verify=True)
        withdrawals_page.loading_indicator.here_then_gone()
        # On the Withdrawal Requests page, click the row for the preprint that was just
        # submitted above. It should be the first in the list since they are sorted
        # newest to oldest.
        withdrawals_page.click_requests_row(provider_id, preprint_node)
        preprint_detail_page = PendingPreprintDetailPage(driver, verify=True)
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button.btn.dropdown-toggle.btn-success')
            )
        )
        # Verify that the Preprint has a Pending status in the status bar
        assert preprint_detail_page.status.text == 'pending'
        # Click the Make decision button to reveal the review options. Then click
        # the Decline radio button, enter a reason in the text box and click the
        # Submit decision button to complete the review.
        preprint_detail_page.make_decision_button.click()
        preprint_detail_page.reject_radio_button.click()
        preprint_detail_page.reason_textarea.clear()
        preprint_detail_page.reason_textarea.send_keys_deliberately(
            'Selenium Testing - Declining Withdrawal Request of Pre-Moderated Preprint'
        )
        preprint_detail_page.submit_decision_button.click()
        # Should end up back on the Reviews Submission page
        assert ReviewsSubmissionsPage(driver, verify=True)
        # Use the api to verify that the Preprint is still published and that its review
        # status is still 'accepted'.
        prep_attr = osf_api.get_preprint_publish_and_review_states(
            preprint_node=preprint_node
        )
        assert prep_attr[0]
        assert prep_attr[1] == 'accepted'
        # Logout and navigate to the Preprint Detail page which should still be publicly
        # accessible.
        logout(driver)
        preprint_page = PreprintDetailPage(driver, guid=preprint_node)
        preprint_page.goto()
        assert PreprintDetailPage(driver, verify=True)
        WebDriverWait(driver, 5).until(EC.visibility_of(preprint_page.title))
        assert preprint_page.title.text == preprint_title
        assert provider_id in driver.current_url

    def test_accept_post_moderated_preprint(
        self, session, driver, log_in_if_not_already
    ):
        """Test the acceptance of a preprint submission to a preprint provider with a
        Post-moderation workflow. In this workflow a preprint is submitted to the
        preprint service provider and is published and publicly accessible upon
        submission.  A moderator can then 'accept' the preprint submission.
        NOTE: In this test case User One is used to login to OSF and must therefore be
        setup through the admin app as a moderator or admin for the Preprint Provider
        being used.  The test will use the OSF api to create a submitted preprint, but
        the preprint will be submitted using the session credentials of User Two so
        that the preprint submitter and moderator are different users.
        """
        # The following Preprint Provider must be setup in each testing environment.
        provider_id = 'selpostmod'
        provider_name = 'Selenium Post-moderation'
        preprint_title = 'OSF Selenium Post-moderation Preprint'

        # NOTE: Using User Two to create the preprint through the api so that the user
        # that submits the preprint is different from the user that accepts or rejects
        # it.
        session_user_two = osf_api.get_user_two_session()
        preprint_node = osf_api.create_preprint(
            session_user_two,
            provider_id=provider_id,
            title=preprint_title,
            license_name='CC0 1.0 Universal',
            subject_name='Engineering',
        )
        # Use the api to verify that the Preprint is already published and that its
        # review status is 'pending'.
        prep_attr = osf_api.get_preprint_publish_and_review_states(
            preprint_node=preprint_node
        )
        assert prep_attr[0]
        assert prep_attr[1] == 'pending'
        # Load Reviews Dashboard page first and then click the Submissions link for the
        # Post-moderation provider to go to that page.
        reviews_dashboard_page = ReviewsDashboardPage(driver)
        reviews_dashboard_page.goto()
        assert ReviewsDashboardPage(driver, verify=True)
        reviews_dashboard_page.loading_indicator.here_then_gone()
        reviews_dashboard_page.click_provider_group_link(provider_name, 'Submissions')
        submissions_page = ReviewsSubmissionsPage(driver, verify=True)
        submissions_page.loading_indicator.here_then_gone()
        # On the Reviews Submissions page, click the row for the preprint that was just
        # submitted above. It should be the first in the list since they are sorted
        # newest to oldest.
        submissions_page.click_submission_row(provider_id, preprint_node)
        preprint_detail_page = PendingPreprintDetailPage(driver, verify=True)
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button.btn.dropdown-toggle.btn-success')
            )
        )
        # Verify that the Preprint has a Pending status in the status bar
        assert preprint_detail_page.status.text == 'pending'
        # Click the Make decision button to reveal the review options. Then click
        # the Accept radio button, enter a reason in the text box and click the
        # Submit decision button to complete the review.
        preprint_detail_page.make_decision_button.click()
        preprint_detail_page.accept_radio_button.click()
        preprint_detail_page.reason_textarea.send_keys_deliberately(
            'Selenium Testing - Accepting Post-Moderated Preprint'
        )
        preprint_detail_page.submit_decision_button.click()
        # Should end up back on the Reviews Submission page
        assert ReviewsSubmissionsPage(driver, verify=True)
        # Use the api to verify that the Preprint is still published and that its review
        # status is now 'accepted'.
        prep_attr = osf_api.get_preprint_publish_and_review_states(
            preprint_node=preprint_node
        )
        assert prep_attr[0]
        assert prep_attr[1] == 'accepted'
        # Logout and navigate to the Preprint Detail page since it is public.
        logout(driver)
        preprint_page = PreprintDetailPage(driver, guid=preprint_node)
        preprint_page.goto()
        assert PreprintDetailPage(driver, verify=True)
        WebDriverWait(driver, 5).until(EC.visibility_of(preprint_page.title))
        assert preprint_page.title.text == preprint_title
        assert provider_id in driver.current_url

    def test_moderator_withdrawal_post_moderated_preprint(
        self, session, driver, log_in_if_not_already
    ):
        """Test the moderator withdrawal of a preprint submission to a Preprint Provider
        with a Post-moderation workflow. In this workflow a preprint is submitted to the
        preprint service provider and is published and publicly accessible upon
        submission.  A moderator can then 'withdraw' the preprint submission and it will
        no longer be publicly accessible.
        NOTE: In this test case User One is used to login to OSF and must therefore be
        setup through the admin app as a moderator or admin for the Preprint Provider
        being used.  The test will use the OSF api to create a submitted preprint, but
        the preprint will be submitted using the session credentials of User Two so
        that the preprint submitter and moderator are different users.
        """
        # The following Preprint Provider must be setup in each testing environment.
        provider_id = 'selpostmod'
        provider_name = 'Selenium Post-moderation'
        preprint_title = 'OSF Selenium Post-moderation Preprint'

        # NOTE: Using User Two to create the preprint through the api so that the user
        # that submits the preprint is different from the user that accepts or rejects
        # it.
        session_user_two = osf_api.get_user_two_session()
        preprint_node = osf_api.create_preprint(
            session_user_two,
            provider_id=provider_id,
            title=preprint_title,
            license_name='CC0 1.0 Universal',
            subject_name='Engineering',
        )
        # Use the api to verify that the Preprint is already published and that its
        # review status is 'pending'.
        prep_attr = osf_api.get_preprint_publish_and_review_states(
            preprint_node=preprint_node
        )
        assert prep_attr[0]
        assert prep_attr[1] == 'pending'
        # Load Reviews Dashboard page first and then click the Submissions link for the
        # Post-moderation provider to go to that page.
        reviews_dashboard_page = ReviewsDashboardPage(driver)
        reviews_dashboard_page.goto()
        assert ReviewsDashboardPage(driver, verify=True)
        reviews_dashboard_page.loading_indicator.here_then_gone()
        reviews_dashboard_page.click_provider_group_link(provider_name, 'Submissions')
        submissions_page = ReviewsSubmissionsPage(driver, verify=True)
        submissions_page.loading_indicator.here_then_gone()
        # On the Reviews Submissions page, click the row for the preprint that was just
        # submitted above. It should be the first in the list since they are sorted
        # newest to oldest.
        submissions_page.click_submission_row(provider_id, preprint_node)
        preprint_detail_page = PendingPreprintDetailPage(driver, verify=True)
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button.btn.dropdown-toggle.btn-success')
            )
        )
        # Verify that the Preprint has a Pending status in the status bar
        assert preprint_detail_page.status.text == 'pending'
        # Click the Make decision button to reveal the review options. Then click
        # the Withdraw radio button, enter a reason in the text box and click the
        # Submit decision button to complete the review.
        preprint_detail_page.make_decision_button.click()
        preprint_detail_page.withdraw_radio_button.click()
        preprint_detail_page.reason_textarea.send_keys_deliberately(
            'Selenium Testing - Withdrawal by Moderator of a Post-Moderated Preprint'
        )
        preprint_detail_page.submit_decision_button.click()
        # Should end up back on the Reviews Submission page
        assert ReviewsSubmissionsPage(driver, verify=True)
        # Use the api to verify that the Preprint is now unpublished and that its
        # review status is now 'withdrawn'.
        prep_attr = osf_api.get_preprint_publish_and_review_states(
            preprint_node=preprint_node
        )
        assert not prep_attr[0]
        assert prep_attr[1] == 'withdrawn'
        # Logout and navigate to the Preprint Detail page. We should see a Withdrawn
        # tombstone page.
        logout(driver)
        preprint_page = PreprintDetailPage(driver, guid=preprint_node)
        preprint_page.goto()
        assert PreprintDetailPage(driver, verify=True)
        WebDriverWait(driver, 5).until(EC.visibility_of(preprint_page.title))
        assert preprint_page.title.text == preprint_title
        assert (
            preprint_page.status_explanation.text == 'This preprint has been withdrawn.'
        )

    def test_approve_withdrawal_request_post_moderated_preprint(
        self, session, driver, log_in_if_not_already
    ):
        """Test the approval of a Withdrawal Request for a preprint submitted and
        accepted by a preprint provider with a Post-moderation workflow. In this
        workflow the moderator will approve/accept the withdrawal request and the
        public preprint will be replaced with a Withdrawn tombstone page in OSF. The
        test will use the OSF api to create a submitted preprint and to accept the
        preprint and create the withdrawal request record. The actual test steps will
        thus start at the point where the moderator takes action from the Reviews
        Dashboard page to approve the withdrawal request.
        NOTE: In this test case User One is used to login to OSF and must therefore be
        setup through the admin app as a moderator or admin for the Preprint Provider
        being used.
        """
        # The following Preprint Provider must be setup in each testing environment.
        provider_id = 'selpostmod'
        provider_name = 'Selenium Post-moderation'
        preprint_title = 'OSF Selenium Post-moderation Preprint'

        # NOTE: Using User Two to create the preprint through the api so that the user
        # that submits the preprint is different from the user that accepts or rejects
        # it.
        session_user_two = osf_api.get_user_two_session()
        preprint_node = osf_api.create_preprint(
            session_user_two,
            provider_id=provider_id,
            title=preprint_title,
            license_name='CC0 1.0 Universal',
            subject_name='Engineering',
        )
        # Set session to None before calling accept_preprint so that the api function
        # will use the default User One session which should have the permissions as
        # a moderator to be able to accept the preprint.
        osf_api.accept_moderated_preprint(session=None, preprint_node=preprint_node)
        # Next use the api to create a withdrawal request (using User Two again)
        osf_api.create_preprint_withdrawal_request(
            session=session_user_two, preprint_node=preprint_node
        )
        # Load Reviews Dashboard page first and then click the Submissions link for the
        # Post-moderation provider to go to that page.
        reviews_dashboard_page = ReviewsDashboardPage(driver)
        reviews_dashboard_page.goto()
        assert ReviewsDashboardPage(driver, verify=True)
        reviews_dashboard_page.loading_indicator.here_then_gone()
        reviews_dashboard_page.click_provider_group_link(provider_name, 'Submissions')
        submissions_page = ReviewsSubmissionsPage(driver, verify=True)
        submissions_page.loading_indicator.here_then_gone()
        # Click the Withdrawal Requests tab
        submissions_page.withdrawal_requests_tab.click()
        withdrawals_page = ReviewsWithdrawalsPage(driver, verify=True)
        withdrawals_page.loading_indicator.here_then_gone()
        # On the Withdrawal Requests page, click the row for the preprint that was just
        # submitted above. It should be the first in the list since they are sorted
        # newest to oldest.
        withdrawals_page.click_requests_row(provider_id, preprint_node)
        preprint_detail_page = PendingPreprintDetailPage(driver, verify=True)
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button.btn.dropdown-toggle.btn-success')
            )
        )
        # Verify that the Preprint has a Pending status in the status bar
        assert preprint_detail_page.status.text == 'pending'
        # Click the Make decision button to reveal the review options. Then click
        # the Approve radio button, enter a reason in the text box and click the
        # Submit decision button to complete the review.
        preprint_detail_page.make_decision_button.click()
        preprint_detail_page.accept_radio_button.click()
        preprint_detail_page.reason_textarea.clear()
        preprint_detail_page.reason_textarea.send_keys_deliberately(
            'Selenium Testing - Approving Withdrawal Request of Post-Moderated Preprint'
        )
        preprint_detail_page.submit_decision_button.click()
        # Should end up back on the Reviews Submission page
        assert ReviewsSubmissionsPage(driver, verify=True)
        # Use the api to verify that the Preprint is not published and that its review
        # status is now 'withdrawn'.
        prep_attr = osf_api.get_preprint_publish_and_review_states(
            preprint_node=preprint_node
        )
        assert not prep_attr[0]
        assert prep_attr[1] == 'withdrawn'
        # Logout and navigate to the Preprint Detail page. We should see a Withdrawn
        # tombstone page.
        logout(driver)
        preprint_page = PreprintDetailPage(driver, guid=preprint_node)
        preprint_page.goto()
        assert PreprintDetailPage(driver, verify=True)
        WebDriverWait(driver, 5).until(EC.visibility_of(preprint_page.title))
        assert preprint_page.title.text == preprint_title
        assert (
            preprint_page.status_explanation.text == 'This preprint has been withdrawn.'
        )

    def test_decline_withdrawal_request_post_moderated_preprint(
        self, session, driver, log_in_if_not_already
    ):
        """Test the declining of a Withdrawal Request for a preprint submitted and
        accepted by a preprint provider with a Post-moderation workflow. In this
        workflow the moderator will decline the withdrawal request and the preprint
        will remain accepted and publicly accessible. The test will use the OSF api
        to create a submitted preprint and to accept the preprint and create the
        withdrawal request record. The actual test steps will thus start at the point
        where the moderator takes action from the Reviews Dashboard page to decline
        the withdrawal request.
        NOTE: In this test case User One is used to login to OSF and must therefore be
        setup through the admin app as a moderator or admin for the Preprint Provider
        being used.
        """
        # The following Preprint Provider must be setup in each testing environment.
        provider_id = 'selpostmod'
        provider_name = 'Selenium Post-moderation'
        preprint_title = 'OSF Selenium Post-moderation Preprint'

        # NOTE: Using User Two to create the preprint through the api so that the user
        # that submits the preprint is different from the user that accepts or rejects
        # it.
        session_user_two = osf_api.get_user_two_session()
        preprint_node = osf_api.create_preprint(
            session_user_two,
            provider_id=provider_id,
            title=preprint_title,
            license_name='CC0 1.0 Universal',
            subject_name='Engineering',
        )
        # Set session to None before calling accept_preprint so that the api function
        # will use the default User One session which should have the permissions as
        # a moderator to be able to accept the preprint.
        osf_api.accept_moderated_preprint(session=None, preprint_node=preprint_node)
        # Next use the api to create a withdrawal request (using User Two again)
        osf_api.create_preprint_withdrawal_request(
            session=session_user_two, preprint_node=preprint_node
        )
        # Load Reviews Dashboard page first and then click the Submissions link for the
        # Pre-moderation provider to go to that page.
        reviews_dashboard_page = ReviewsDashboardPage(driver)
        reviews_dashboard_page.goto()
        assert ReviewsDashboardPage(driver, verify=True)
        reviews_dashboard_page.loading_indicator.here_then_gone()
        reviews_dashboard_page.click_provider_group_link(provider_name, 'Submissions')
        submissions_page = ReviewsSubmissionsPage(driver, verify=True)
        submissions_page.loading_indicator.here_then_gone()
        # Click the Withdrawal Requests tab
        submissions_page.withdrawal_requests_tab.click()
        withdrawals_page = ReviewsWithdrawalsPage(driver, verify=True)
        withdrawals_page.loading_indicator.here_then_gone()
        # On the Withdrawal Requests page, click the row for the preprint that was just
        # submitted above. It should be the first in the list since they are sorted
        # newest to oldest.
        withdrawals_page.click_requests_row(provider_id, preprint_node)
        preprint_detail_page = PendingPreprintDetailPage(driver, verify=True)
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button.btn.dropdown-toggle.btn-success')
            )
        )
        # Verify that the Preprint has a Pending status in the status bar
        assert preprint_detail_page.status.text == 'pending'
        # Click the Make decision button to reveal the review options. Then click
        # the Decline radio button, enter a reason in the text box and click the
        # Submit decision button to complete the review.
        preprint_detail_page.make_decision_button.click()
        preprint_detail_page.reject_radio_button.click()
        preprint_detail_page.reason_textarea.clear()
        preprint_detail_page.reason_textarea.send_keys_deliberately(
            'Selenium Testing - Declining Withdrawal Request of Post-Moderated Preprint'
        )
        preprint_detail_page.submit_decision_button.click()
        # Should end up back on the Reviews Submission page
        assert ReviewsSubmissionsPage(driver, verify=True)
        # Use the api to verify that the Preprint is still published and that its review
        # status is still 'accepted'.
        prep_attr = osf_api.get_preprint_publish_and_review_states(
            preprint_node=preprint_node
        )
        assert prep_attr[0]
        assert prep_attr[1] == 'accepted'
        # Logout and navigate to the Preprint Detail page which should still be publicly
        # accessible.
        logout(driver)
        preprint_page = PreprintDetailPage(driver, guid=preprint_node)
        preprint_page.goto()
        assert PreprintDetailPage(driver, verify=True)
        WebDriverWait(driver, 5).until(EC.visibility_of(preprint_page.title))
        assert preprint_page.title.text == preprint_title
        assert provider_id in driver.current_url


@markers.core_functionality
class TestPreprintSearch:
    @markers.two_minute_drill
    @markers.smoke_test
    def test_search_results_exist(self, driver, landing_page):
        landing_page.search_button.click()
        discover_page = PreprintDiscoverPage(driver, verify=True)
        discover_page.loading_indicator.here_then_gone()
        assert len(discover_page.search_results) > 0

    def test_preprint_detail_page(self, driver):
        discover_page = PreprintDiscoverPage(driver)
        discover_page.goto()
        assert PreprintDiscoverPage(driver, verify=True)
        if not settings.PRODUCTION:
            # Since all of the testing environments use the same SHARE server, we need
            # to enter a value in the search input box that will ensure that the results
            # are specific to the current environment.  We can do this by searching for
            # the test environment url in the identifiers metadata field.
            environment_url = settings.OSF_HOME[
                8:
            ]  # Need to strip out "https://" from the url
            search_text = environment_url
            discover_page.search_box.send_keys_deliberately(search_text)
            discover_page.search_box.send_keys(Keys.ENTER)
            if settings.STAGE2:
                # Stage 2 has a lot of old preprint data that is still listed in search
                # results but does not actually have preprint detail pages so we need to
                # sort the results so that the newest preprints are listed first.
                discover_page.sort_button.click()
                discover_page.sort_option_newest_to_oldest.click()
        discover_page.loading_indicator.here_then_gone()
        search_results = discover_page.search_results
        assert search_results
        # Click on first entry in search results to open the Preprint Detail page
        search_results[0].find_element_by_css_selector(
            'a[data-test-search-result-card-title]'
        ).click()
        main_window = switch_to_new_tab(driver)
        assert PreprintDetailPage(driver, verify=True)
        close_current_tab(driver, main_window)


@markers.smoke_test
@markers.core_functionality
class TestPreprintMetrics:
    @pytest.fixture(scope='session')
    def latest_preprint_node(self):
        """Return the node id of the latest preprint submitted in the given environment"""
        return osf_api.get_most_recent_preprint_node_id()

    def test_preprint_views_count(self, driver, latest_preprint_node):
        """Test the Views Count functionality on the Preprint Detail page by getting
        the views count for a preprint using the api and comparing it to the views
        count value displayed on the page. Also verifying that the views count will
        be incremented if the page is reloaded (only in testing environments).
        """
        api_views_count = osf_api.get_preprint_views_count(node_id=latest_preprint_node)
        preprint_page = PreprintDetailPage(driver, guid=latest_preprint_node)
        preprint_page.goto()
        assert PreprintDetailPage(driver, verify=True)
        match = re.search(
            r'Views: (\d+) \| Downloads:', preprint_page.views_downloads_counts.text
        )
        assert match is not None
        page_views_count = int(match.group(1))
        assert api_views_count == page_views_count
        # Don't reload the page in Production since we don't want to artificially
        # inflate the metrics
        if not settings.PRODUCTION:
            # Verify that the views count from the api increases after we reload the
            # page. NOTE: Due to timing, getting the count from the api again could
            # result in the count being either 1 or 2 greater than the previous count.
            # The initial load of the page above adds 1 to the views count, and the
            # following reload adds a 2nd view to the count.  But the update to the
            # database can take a couple of seconds, so immediately accessing the api
            # to get the count below may not show the 2nd view.  Hence we are just
            # checking that the views count did increase but not by how much.
            # Unfortunately this means that we are not checking for any issues like
            # double-counting.
            preprint_page.reload()
            assert (
                osf_api.get_preprint_views_count(node_id=latest_preprint_node)
                > api_views_count
            )

    def test_preprint_downloads_count(self, driver, latest_preprint_node):
        """Test the Downloads Count functionality on the Preprint Detail page by
        getting the downloads count for a preprint using the api and comparing it to
        the downloads count value displayed on the page. Also verifying that the
        downloads count will be incremented when the downloads button on the page is
        clicked (only in testing environments).
        """
        api_downloads_count = osf_api.get_preprint_downloads_count(
            node_id=latest_preprint_node
        )
        preprint_page = PreprintDetailPage(driver, guid=latest_preprint_node)
        preprint_page.goto()
        assert PreprintDetailPage(driver, verify=True)
        page_downloads_count = int(
            preprint_page.views_downloads_counts.text.split('Downloads:')[1]
        )
        assert api_downloads_count == page_downloads_count
        # Don't download the Preprint in Production since we don't want to artificially
        # inflate the metrics
        if not settings.PRODUCTION:
            # Verify that the downloads count from the api increases by 1 after we
            # download the document.
            preprint_page.download_button.click()
            assert (
                osf_api.get_preprint_downloads_count(node_id=latest_preprint_node)
                == api_downloads_count + 1
            )


@pytest.fixture(scope='session')
def providers():
    """Return all preprint providers."""
    return osf_api.get_providers_list()


@pytest.fixture(scope='session')
def custom_providers():
    """Return the API data of all preprint providers with custom domains."""
    providers = osf_api.get_providers_list()
    return [
        provider
        for provider in providers
        if provider['attributes']['domain_redirect_enabled']
    ]


@markers.core_functionality
class TestProvidersWithCustomDomains:
    @pytest.fixture(
        params=custom_providers(), ids=[prov['id'] for prov in custom_providers()]
    )
    def provider(self, request):
        return request.param

    def test_landing_page_loads(self, driver, provider):
        PreprintLandingPage(driver, provider=provider).goto()

    def test_discover_page_loads(self, driver, provider):
        PreprintDiscoverPage(driver, provider=provider).goto()

    @pytest.mark.usefixtures('must_be_logged_in')
    def test_submit_page_loads(self, driver, provider):
        allow_submissions = osf_api.get_provider_submission_status(provider)
        if allow_submissions:
            PreprintSubmitPage(driver, provider=provider).goto()
        else:
            landing_page = PreprintLandingPage(driver, provider=provider)
            landing_page.goto()
            assert 'submit' not in landing_page.submit_navbar.text
            assert not landing_page.submit_button.present()


@markers.smoke_test
@pytest.mark.skipif(
    not settings.PRODUCTION,
    reason='Most of the Branded Preprint Provider pages in test environments have no preprints',
)
class TestBrandedProviders:
    """This class only runs in Production for all Branded Providers"""

    @pytest.fixture(params=providers(), ids=[prov['id'] for prov in providers()])
    def provider(self, request):
        return request.param

    def test_detail_page(self, session, driver, provider):
        """Test a preprint detail page by grabbing the first search result from the discover page."""
        discover_page = BrandedPreprintsDiscoverPage(driver, provider=provider)

        # This fails only in firefox because of selenium incompatibilities with right-left languages
        if 'firefox' in find_current_browser(driver) and 'arabixiv' in provider['id']:
            discover_page.url_addition += '?q=Analysis'

        # As of January 24, 2022, the Engineering Archive ('engrxiv') preprint provider
        # has switched away from using OSF as their preprint service.  Therefore the
        # web page that OSF automatically redirects to is no longer based on the OSF
        # Preprints landing/discover page design.  However, they remain in our active
        # preprint provider list in the OSF api due to legal issues that are still being
        # worked out.  The best guess is that the transition will be completed (and
        # engrxiv removed from the api list) by the end of the first quarter of 2022
        # (i.e. end of March).  So to prevent this test from failing in Production
        # every night for 'engrxiv' we are going to skip the following steps for this
        # provider.
        # UPDATE 10/26/2022 - the status of 'engrxiv' has not changed and now another
        # provider - 'ecoevorxiv' is also leaving OSF.
        # UPDATE 10/13/2023 - After the Search Improvements project release, OSF and other providers
        # that have moved away from OSF now redirect to https://osf.io/search?q=&resourceType=Preprint&q=
        providers_leaving_OSF = ['ecoevorxiv', 'engrxiv', 'livedata', 'osf']
        if provider['id'] not in providers_leaving_OSF:
            discover_page.goto()
            discover_page.verify()
            # add OSF consent cookie to get rid of the banner at the bottom of the page which can get in the way
            # when we have to scroll down to click the first preprint listing
            driver.add_cookie({'name': 'osf_cookieconsent', 'value': '1'})
            discover_page.reload()
            discover_page.loading_indicator.here_then_gone()

            if osf_api.get_providers_total(provider['id'], session=session):
                search_results = discover_page.search_results
                assert search_results
                first_preprint = search_results[0].find_element_by_css_selector(
                    '[data-test-search-result-card-title]'
                )

                # Save the target preprints link and get the guid in the href attribute
                # Note: This test currently only runs on prod so this regex does not support test env urls
                first_preprint_link = first_preprint.get_attribute('href')
                match = re.search(
                    r'(^https://osf\.io/([a-z0-9]{5}))', first_preprint_link
                )
                preprint_guid = match.group(2)

                first_preprint.click()
                main_window = switch_to_new_tab(driver)

                PreprintDetailPage(driver, verify=True)
                assert provider['id'] in driver.current_url
                assert preprint_guid in driver.current_url

                close_current_tab(driver, main_window)

            elif not provider['attributes']['additional_providers']:
                # Some Preprint Providers may also display preprints from other sources not
                # just OSF. So we do not want to assert that there are No Results when there
                # may be results from non-OSF providers.
                assert discover_page.no_results
