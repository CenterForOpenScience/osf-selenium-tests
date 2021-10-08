import pytest
import markers
from pages.registrations import MyRegistrationsPage
from pages.registries import RegistrationAddNewPage, RegistrationDraftPage, RegistrationDetailPage


@markers.smoke_test
class TestMyRegistrationsPageEmpty:
    """This test covers the My Registrations page: https://{home}/registries/my-registrations
    """
    @pytest.fixture()
    def registrations_page(self, driver, must_be_logged_in):
        my_registrations_page = MyRegistrationsPage(driver)
        my_registrations_page.goto()
        return my_registrations_page

    def test_no_drafts(self, driver, registrations_page):
        registrations_page.drafts_tab.click()
        assert "You don't have any draft registrations." in registrations_page.no_drafts_message.text
        registrations_page.create_a_registration_button_drafts.click()
        RegistrationAddNewPage(driver, verify=True)

    def test_no_registrations(self, driver, registrations_page):
        registrations_page.submissions_tab.click()
        assert "You don't have any submitted registrations." in registrations_page.no_submissions_message.text
        registrations_page.create_a_registration_button_submitted.click()
        RegistrationAddNewPage(driver, verify=True)


@markers.smoke_test
class TestMyRegistrationsUserTwo:
    """User two has a public registration and a registration in the draft state for test purposes.
    """
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
