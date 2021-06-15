import pytest
import markers
import settings

from pages.landing import LandingPage
from pages.register import RegisterPage
from pages.login import (
    LoginPage,
    InstitutionalLoginPage,
    ForgotPasswordPage,
    UnsupportedInstitutionLoginPage,
    GenericCASPage,
    login,
)

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

@pytest.fixture
def login_page(driver):
    login_page = LoginPage(driver)
    login_page.goto()
    return login_page


class TestLoginPage:

    @markers.core_functionality
    def test_institutional_login(self, driver, login_page):
        """Check that you arrive on the institutional login page and the institution dropdown is populated.
        We can't actually test institutional login.
        """
        login_page.institutional_login_button.click()
        institutional_login_page = InstitutionalLoginPage(driver, verify=True)
        assert len(institutional_login_page.dropdown_options) > 1

    @markers.core_functionality
    def test_orcid_login(self, driver, login_page):
        """Check that you arrive on the orcid login page.
        """
        login_page.orcid_login_button.click()

        # If user is logged out of ORCID, ORCID's Oauth service will use
        # redirect link before landing on ORCID sign in page
        WebDriverWait(driver, 10).until(EC.url_contains('https://orcid.org/signin'))

        # Oauth will redirect to callback url with "error" if anything goes wrong
        assert 'error' not in driver.current_url

    def test_osf_home_link(self, driver, login_page):
        login_page.osf_home_link.click()
        assert LandingPage(driver, verify=True)

    def test_sign_up_button(self, driver, login_page):
        login_page.sign_up_button.click()
        assert RegisterPage(driver, verify=True)

    def test_reset_password_link(self, driver, login_page):
        login_page.reset_password_link.click()
        assert ForgotPasswordPage(driver, verify=True)

    def test_need_help_link(self, driver, login_page):
        login_page.need_help_link.click()
        assert 'https://help.osf.io' and 'Sign-in-to-OSF' in driver.current_url

    def test_cos_footer_link(self, driver, login_page):
        login_page.cos_footer_link.click()
        assert driver.current_url == 'https://www.cos.io/'

    def test_terms_of_use_footer_link(self, driver, login_page):
        login_page.terms_of_use_footer_link.click()
        assert driver.current_url == 'https://github.com/CenterForOpenScience/cos.io/blob/master/TERMS_OF_USE.md'

    def test_privacy_policy_footer_link(self, driver, login_page):
        login_page.privacy_policy_footer_link.click()
        assert driver.current_url == 'https://github.com/CenterForOpenScience/cos.io/blob/master/PRIVACY_POLICY.md'

    def test_status_footer_link(self, driver, login_page):
        login_page.status_footer_link.click()
        assert driver.current_url == 'https://status.cos.io/'


class TestGenericPages:
    """Generic pages have no service in the login/logout url. Typically users should not be able to access
    these pages through the standard authentication workflow. The tests in this class manually manipulate the
    urls used in order to get to these pages so that we can verify that they do function just in case they
    are ever needed.
    """

    def test_generic_logged_in_page(self, driver, must_be_logged_in):
        """Test the generic CAS logged in page by manually navigating to a CAS page without a service in the url
        """
        driver.get(settings.CAS_DOMAIN + '/login')
        logged_in_page = GenericCASPage(driver, verify=True)
        assert logged_in_page.auto_redirect_message.text == "Auto-redirection didn't happen ..."
        assert logged_in_page.status_message.text == 'Login successful'

    def test_generic_logged_out_page(self, driver):
        """Test the generic CAS logged out page by manually navigating to a CAS page without a service in the url
        """
        driver.get(settings.CAS_DOMAIN + '/logout')
        logged_out_page = GenericCASPage(driver, verify=True)
        assert logged_out_page.auto_redirect_message.text == "Auto-redirection didn't happen ..."
        assert logged_out_page.status_message.text == 'Logout successful'


class TestLoginErrors:
    """Test the inline error messages on the CAS login page when user enters invalid login data
    """

    def test_missing_email(self, driver, login_page):
        login_page.submit_button.click()
        assert login_page.login_error_message.text == 'Email is required.'

    def test_missing_password(self, driver, login_page):
        login_page.username_input.send_keys_deliberately('foo')
        login_page.submit_button.click()
        assert login_page.login_error_message.text == 'Password is required.'

    def test_invalid_email_and_password(self, driver, login_page):
        login_page.username_input.send_keys_deliberately('foo')
        login_page.password_input.send_keys_deliberately('foo')
        login_page.submit_button.click()
        assert login_page.login_error_message.text == 'The email or password you entered is incorrect.'

    def test_invalid_password(self, driver, login_page):
        login_page.username_input.send_keys_deliberately(settings.USER_ONE)
        login_page.password_input.send_keys_deliberately('foo')
        login_page.submit_button.click()
        assert login_page.login_error_message.text == 'The email or password you entered is incorrect.'


class TestCustomExceptionPages:
    """CAS has several customized exception pages which share the same style and appearance as the CAS login pages.
    Not all of them can be easily tested. Those that can will require the manipulation of urls to reach the pages.
    """

    def test_service_not_authorized_page(self, driver):
        """Test the Service not authorized exception page by having an invalid service in the url
        """
        driver.get(settings.CAS_DOMAIN + '/login?service=https://noservice.osf.io/')
        exception_page = GenericCASPage(driver, verify=True)
        assert exception_page.navbar_brand.text == 'OSF HOME'
        assert exception_page.status_message.text == 'Service not authorized'

    def test_verification_key_login_failed_page(self, driver):
        """Test the Verification key login failed exception page by having an invalid verification_key parameter
        in the url
        """
        driver.get(settings.CAS_DOMAIN + '/login?service=' + settings.CAS_DOMAIN + '/login/?next=' + settings.CAS_DOMAIN + '/&username=' + settings.USER_ONE + '&verification_key=foo')
        exception_page = GenericCASPage(driver, verify=True)
        assert exception_page.navbar_brand.text == 'OSF HOME'
        assert exception_page.status_message.text == 'Verification key login failed'

    def test_flow_less_page_not_found_page(self, driver):
        """Test the Page Not Found exception page by having an invalid path in the url. CAS only supports 3 valid paths:
        /login, /logout, or /oauth.
        """
        driver.get(settings.CAS_DOMAIN + '/nopath')
        exception_page = GenericCASPage(driver, verify=True)
        # Since this exception page is flow-less (a.k.a. OSF unaware) the navbar will display OSF CAS instead of OSF HOME
        assert exception_page.navbar_brand.text == 'OSF CAS'
        assert exception_page.status_message.text == 'Page Not Found'

    @markers.dont_run_on_prod
    def test_account_not_confirmed_page(self, driver):
        login(driver, user=settings.UNCONFIRMED_USER, password=settings.UNCONFIRMED_USER_PASSWORD)
        exception_page = GenericCASPage(driver, verify=True)
        assert exception_page.navbar_brand.text == 'OSF HOME'
        assert exception_page.status_message.text == 'Account not confirmed'

    @markers.dont_run_on_prod
    def test_account_disabled_page(self, driver):
        login(driver, user=settings.DEACTIVATED_USER, password=settings.DEACTIVATED_USER_PASSWORD)
        exception_page = GenericCASPage(driver, verify=True)
        assert exception_page.navbar_brand.text == 'OSF HOME'
        assert exception_page.status_message.text == 'Account disabled'


class TestInstitutionLoginPage:

    @pytest.fixture
    def institution_login_page(self, driver):
        institution_login_page = InstitutionalLoginPage(driver)
        institution_login_page.goto()
        return institution_login_page

    def test_enable_sign_in_button(self, driver, institution_login_page):
        """When you first go to the Institution Login page the Sign In button is disabled. It
        only becomes enabled after selecting an institution from the dropdown list.
        """
        assert driver.find_element(By.ID, 'institutionSubmit').get_property('disabled')
        institution_select = Select(institution_login_page.institution_dropdown)
        # select the first institution in the dropdown - index 0 is the message '-- select an institution --'
        institution_select.select_by_index(1)
        assert institution_login_page.sign_in_button.is_enabled()

    def test_osf_home_link(self, driver, institution_login_page):
        institution_login_page.osf_home_link.click()
        assert LandingPage(driver, verify=True)

    def test_sign_up_button(self, driver, institution_login_page):
        institution_login_page.sign_up_button.click()
        assert RegisterPage(driver, verify=True)

    def test_cant_find_institution_link(self, driver, institution_login_page):
        institution_login_page.cant_find_institution_link.click()
        assert UnsupportedInstitutionLoginPage(driver, verify=True)

    def test_need_help_link(self, driver, institution_login_page):
        institution_login_page.need_help_link.click()
        assert 'https://help.osf.io' and 'Sign-in-to-OSF' in driver.current_url

    def test_sign_in_with_osf_link(self, driver, institution_login_page):
        institution_login_page.sign_in_with_osf_link.click()
        assert LoginPage(driver, verify=True)

    def test_cos_footer_link(self, driver, institution_login_page):
        institution_login_page.cos_footer_link.click()
        assert driver.current_url == 'https://www.cos.io/'

    def test_terms_of_use_footer_link(self, driver, institution_login_page):
        institution_login_page.terms_of_use_footer_link.click()
        assert driver.current_url == 'https://github.com/CenterForOpenScience/cos.io/blob/master/TERMS_OF_USE.md'

    def test_privacy_policy_footer_link(self, driver, institution_login_page):
        institution_login_page.privacy_policy_footer_link.click()
        assert driver.current_url == 'https://github.com/CenterForOpenScience/cos.io/blob/master/PRIVACY_POLICY.md'

    def test_status_footer_link(self, driver, institution_login_page):
        institution_login_page.status_footer_link.click()
        assert driver.current_url == 'https://status.cos.io/'
