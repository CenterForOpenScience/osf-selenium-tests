import pytest
from pages.registrations import MyRegistrationsPage
from pages.registries import RegistrationAddNewPage


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
