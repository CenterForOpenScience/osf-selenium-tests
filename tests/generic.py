import pytest

import markers
import settings


class CreateUserMixin:
    """Mixin used to inject user creation test"""

    @pytest.fixture()
    def page(self, driver):
        raise NotImplementedError()

    @markers.dont_run_on_prod
    @pytest.mark.skipif(
        settings.TEST,
        reason='There is a real recapcha on test. Robots cannot create users there.',
    )
    def test_create_user(self, page, fake):

        name = fake.name()
        email = settings.NEW_USER_EMAIL.format(
            ''.join(name.split())
        )  # Add name with no spaces to end of email
        password = fake.sentence()

        page.scroll_into_view(page.sign_up_form.sign_up_button.element)

        page.sign_up_form.name_input.send_keys(name)
        page.sign_up_form.email_one_input.send_keys(email)
        page.sign_up_form.email_two_input.send_keys(email)
        page.sign_up_form.password_input.send_keys(password)
        page.sign_up_form.terms_of_service_checkbox.click()
        page.sign_up_form.click_recaptcha()
        page.sign_up_form.sign_up_button.click()
        assert page.sign_up_form.registration_success.present()
