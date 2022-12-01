import re

import pytest
from faker import Faker
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import api
import markers
from api import osf_api
from pages.registrations import MyRegistrationsPage
from pages.registries import (
    JustificationReviewForm,
    RegistrationAddNewPage,
    RegistrationDetailPage,
    RegistrationDraftPage,
    RegistrationJustificationForm,
)


@markers.smoke_test
@markers.core_functionality
class TestMyRegistrationsPageEmpty:
    """This test covers the My Registrations page: https://{home}/registries/my-registrations"""

    @pytest.fixture()
    def registrations_page(self, driver, must_be_logged_in):
        my_registrations_page = MyRegistrationsPage(driver)
        my_registrations_page.goto()
        return my_registrations_page

    def test_no_drafts(self, driver, registrations_page):
        registrations_page.drafts_tab.click()
        assert (
            "You don't have any draft registrations."
            in registrations_page.no_drafts_message.text
        )
        registrations_page.create_a_registration_button_drafts.click()
        RegistrationAddNewPage(driver, verify=True)

    def test_no_registrations(self, driver, registrations_page):
        registrations_page.submissions_tab.click()
        assert (
            "You don't have any submitted registrations."
            in registrations_page.no_submissions_message.text
        )
        registrations_page.create_a_registration_button_submitted.click()
        RegistrationAddNewPage(driver, verify=True)


@markers.smoke_test
@markers.core_functionality
class TestMyRegistrationsUserTwo:
    """User two has a public registration and a registration in the draft state for test purposes."""

    @pytest.fixture()
    def registrations_page(self, driver, must_be_logged_in_as_user_two):
        my_registrations_page = MyRegistrationsPage(driver)
        my_registrations_page.goto()
        return my_registrations_page

    def test_drafts_tab(self, driver, registrations_page):
        registrations_page.drafts_tab.click()
        registrations_page.draft_registration_title.click()
        RegistrationDraftPage(driver, verify=True)

    def test_submissions_tab(self, driver, registrations_page):
        registrations_page.submissions_tab.click()
        registrations_page.public_registration_title.click()
        RegistrationDetailPage(driver, verify=True)


@markers.dont_run_on_prod
@markers.core_functionality
class TestRegistrationsVersioning:
    """This test navigates the test user through the entire workflow for updating a registration by creating a new version"""

    def get_registration_version_draft_id(self, href):
        match = re.search(
            r'([a-z0-9]{4,8})\.osf\.io\/registries\/revisions/([a-z0-9]{24})\/review',
            href,
        )

        # Group 1 = Test Domain
        # Group 2 = Draft ID (24 characters long)
        return match.group(2)

    def delete_registration_version_draft(self, session_user_two, registration_card):
        continue_button = registration_card.find_element_by_css_selector(
            '[data-test-view-changes-button]'
        )
        url = continue_button.get_attribute('href')
        draft_id = self.get_registration_version_draft_id(url)
        api.osf_api.delete_registration_version_draft(session_user_two, draft_id)

    def test_versioning_workflow(self, driver, must_be_logged_in_as_user_two):
        my_registrations_page = MyRegistrationsPage(driver)
        my_registrations_page.goto()
        my_registrations_page.loading_indicator.here_then_gone()

        # Check for leftover registration version update in progress and delete if present
        registration_card = my_registrations_page.get_registration_card_by_title(
            'Versioning'
        )
        try:
            if registration_card.find_element_by_css_selector(
                '[data-test-view-changes-button]'
            ):
                self.delete_registration_version_draft(
                    osf_api.get_user_two_session(), registration_card
                )
                my_registrations_page.reload()
                my_registrations_page.loading_indicator.here_then_gone()
                # Re-assign locators because they become stale after a reload()
                my_registrations_page = MyRegistrationsPage(driver)
                registration_card = (
                    my_registrations_page.get_registration_card_by_title('Versioning')
                )

        except NoSuchElementException:
            pass
        except AttributeError:
            pass

        my_registrations_page.update_button = (
            registration_card.find_element_by_css_selector('[data-test-update-button]')
        )
        my_registrations_page.update_button.click()
        my_registrations_page.update_registration_dialogue.present()
        my_registrations_page.update_registration_dialogue_next.click()

        justification_page = RegistrationJustificationForm(driver, verify=True)
        justification_page.justification_textbox.click()
        justification_page.justification_textbox.send_keys(
            'This justification is provided by selenium test automation.'
        )

        justification_page.navbar_review.click()

        # Wait for justification field to update from "No Justification provided." to summary_paragraph
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element(
                (
                    By.CSS_SELECTOR,
                    'p[data-test-review-response="revisionJustification"]',
                ),
                'selenium',
            )
        )

        justification_page.navbar_summary.click()
        fake = Faker()
        summary_paragraph = fake.sentence(nb_words=20)
        justification_page.summary_textbox.click()
        justification_page.summary_textbox.clear()
        justification_page.summary_textbox.send_keys(summary_paragraph)
        justification_page.summary_review_button.click()

        # Wait for justification field to update from "No Justification provided." to summary_paragraph
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element(
                (
                    By.CSS_SELECTOR,
                    'p[data-test-revised-responses-list]',
                ),
                'Provide a narrative summary of what is contained in this registration or how it differs from prior '
                'registrations. If this project contains documents for a preregistration, please note that here',
            )
        )

        justification_page.submit_revision.click()
        justification_page.accept_changes.click()
        justification_page.toast_message.here_then_gone()

        justification_review_page = JustificationReviewForm(driver, verify=True)
        justification_review_page.link_to_registration.click()

        registration_detail_page = RegistrationDetailPage(driver, verify=True)
        registration_detail_page.reload()

        assert summary_paragraph in registration_detail_page.narrative_summary.text

    def test_delete_versioning(self, driver, must_be_logged_in_as_user_two):
        my_registrations_page = MyRegistrationsPage(driver)
        my_registrations_page.goto()
        my_registrations_page.loading_indicator.here_then_gone()

        # Check for leftover registration version update in progress and delete if present
        registration_card = my_registrations_page.get_registration_card_by_title(
            'Versioning'
        )
        try:
            if registration_card.find_element_by_css_selector(
                '[data-test-view-changes-button]'
            ):
                self.delete_registration_version_draft(
                    osf_api.get_user_two_session(), registration_card
                )
                my_registrations_page.reload()
                my_registrations_page.loading_indicator.here_then_gone()
                # Re-assign locators because they become stale after a reload()
                my_registrations_page = MyRegistrationsPage(driver)
                registration_card = (
                    my_registrations_page.get_registration_card_by_title('Versioning')
                )
        except NoSuchElementException:
            pass
        except AttributeError:
            pass

        my_registrations_page.view_button = (
            registration_card.find_element_by_css_selector('[data-test-view-button]')
        )
        my_registrations_page.view_button.click()
        registration_detail_page = RegistrationDetailPage(driver)

        # Store the narrative summary text of the most recent update
        latest_update = registration_detail_page.narrative_summary.text

        # Start the new version update
        registration_detail_page.updates_dropdown.click()
        registration_detail_page.update_registration_button.click()
        registration_detail_page.update_registration_dialogue.present()
        registration_detail_page.update_registration_dialogue_next.click()

        # Cancel the new version update from the draft page
        justification_page = RegistrationJustificationForm(driver, verify=True)
        justification_page.cancel_update_button.click()
        justification_page.cancel_update_modal.present()
        justification_page.confirm_cancel_button.click()

        # Use the dropdown modal to verify an update is NOT in progress and the user can start a new version.
        registration_detail_page = RegistrationDetailPage(driver, verify=True)
        registration_detail_page.updates_dropdown.click()
        registration_detail_page.update_registration_button.present()

        assert latest_update in registration_detail_page.narrative_summary.text
