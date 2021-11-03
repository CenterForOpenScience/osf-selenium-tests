import pytest
import ipdb
from faker import Faker

import markers
from pages.registrations import MyRegistrationsPage
from pages.registries import (
    RegistrationAddNewPage,
    RegistrationDetailPage,
    RegistrationDraftPage,
    RegistrationJustificationForm,
    JustificationReviewForm,
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

    def test_versioning_workflow(self, driver, must_be_logged_in):
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

        ### BUG HERE: User needs to return to justification page for validation ###
        justification_page.navbar_justification.click()
        justification_page.navbar_review.click()

        justification_page.submit_revision.click()
        justification_page.accept_changes.click()

        JustificationReviewForm(driver, verify=True)
        review_form = JustificationReviewForm(driver)
        review_form.link_to_registration.click()

        registration_detail_page = RegistrationDetailPage(driver)
        assert summary_paragraph in registration_detail_page.narrative_summary.text
