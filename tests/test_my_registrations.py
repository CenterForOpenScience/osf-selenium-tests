import time

import pytest
from faker import Faker
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import markers
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


class TestRegistrationsVersioning:
    """This test navigates the test user through the entire workflow for updating a registration by creating a new version"""

    def test_versioning_workflow(self, driver, must_be_logged_in_as_user_two):
        my_registrations_page = MyRegistrationsPage(driver)
        my_registrations_page.goto()
        my_registrations_page.update_button.click()
        my_registrations_page.update_registration_dialogue.present()
        my_registrations_page.update_registration_dialogue_next.click()

        RegistrationJustificationForm(driver, verify=True)
        justification_page = RegistrationJustificationForm(driver)
        justification_page.justification_textbox.click()
        justification_page.justification_textbox.send_keys('This justification is provided by selenium test automation.')
        justification_page.justification_next_button.click()

        fake = Faker()
        summary_paragraph = fake.sentence(nb_words=20)
        justification_page.summary_textbox.click()
        justification_page.summary_textbox.clear()
        justification_page.summary_textbox.send_keys(summary_paragraph)
        justification_page.summary_review_button.click()

        # Wait for justification field to update from "No Justification provided." to summary_paragraph
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, 'p[data-test-review-response="revisionJustification"]'), 'selenium'
            )
        )
        # After the justification field updates, the front end needs a second before becoming usable.
        # If we click the submit button before background process have completed,
        # we get a red toast message that reads 'Your decision was not recorded.'
        time.sleep(2)
        justification_page.submit_revision.click()
        justification_page.accept_changes.click()

        JustificationReviewForm(driver, verify=True)
        review_form = JustificationReviewForm(driver)
        review_form.link_to_registration.click()

        registration_detail_page = RegistrationDetailPage(driver)
        # The registration detail page needs to be refreshed for the changes to take effect.
        driver.refresh()
        assert summary_paragraph in registration_detail_page.narrative_summary.text

    def test_delete_versioning(self, driver, must_be_logged_in_as_user_two):
        my_registrations_page = MyRegistrationsPage(driver)
        my_registrations_page.goto()
        my_registrations_page.view_button.click()
        registration_detail_page = RegistrationDetailPage(driver)

        # Store the narrative summary text of the most recent update
        latest_update = registration_detail_page.narrative_summary.text

        # Start the new version update
        registration_detail_page.updates_dropdown.click()
        registration_detail_page.update_registration_button.click()
        my_registrations_page.update_registration_dialogue.present()
        my_registrations_page.update_registration_dialogue_next.click()

        # Cancel the new version update from the draft page
        RegistrationJustificationForm(driver, verify=True)
        justification_page = RegistrationJustificationForm(driver)
        justification_page.cancel_update_button.click()
        justification_page.cancel_update_modal.present()
        justification_page.confirm_cancel_button.click()

        # Use the dropdown modal to verify an update is NOT in progress and the user can start a new version.
        RegistrationDetailPage(driver, verify=True)
        registration_detail_page = RegistrationDetailPage(driver)
        registration_detail_page.updates_dropdown.click()
        registration_detail_page.update_registration_button.present()

        assert latest_update in registration_detail_page.narrative_summary.text
