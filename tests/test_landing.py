import pytest
import markers
import settings

from pages.landing import LandingPage

@pytest.fixture()
def landing_page(driver):
    landing_page = LandingPage(driver)
    landing_page.goto()
    return landing_page


class TestLandingPage:

    @pytest.mark.skip(reason='These tests will not work until the new sign up page comes out. h/t James!')
    @markers.dont_run_on_prod
    @markers.core_functionality
    def test_create_user(self, driver, landing_page, fake):

        name = fake.name()
        email = settings.NEW_USER_EMAIL.format(''.join(name.split()))  # Add name with no spaces to end of email
        password = fake.sentence()
        landing_page.name_input.send_keys(name)
        landing_page.email_one_input.send_keys(email)
        landing_page.email_two_input.send_keys(email)
        landing_page.password_input.send_keys(password)
        landing_page.terms_of_service_checkbox.click()
        landing_page.sign_up_button.click()
        assert landing_page.registration_success.present()
