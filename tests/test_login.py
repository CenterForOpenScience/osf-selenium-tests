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


class TestLoginWorkflow:

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
        assert driver.current_url == 'https://help.osf.io/hc/en-us/articles/360019737194-Sign-in-to-OSF'

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
        assert driver.current_url == 'https://help.osf.io/hc/en-us/articles/360019737194-Sign-in-to-OSF'

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
