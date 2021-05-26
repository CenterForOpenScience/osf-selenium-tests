import pytest
import markers

from pages.login import LoginPage, InstitutionalLoginPage, ForgotPasswordPage
from pages.landing import LandingPage
from pages.register import RegisterPage

from selenium.webdriver.support import expected_conditions as EC
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
