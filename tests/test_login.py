import markers

from pages.login import LoginPage, InstitutionalLoginPage

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class TestLoginWorkflow:

    @markers.core_functionality
    def test_institutional_login(self, driver):
        """Check that you arrive on the institutional login page and the institution dropdown is populated.
        We can't actually test institutional login.
        """
        login_page = LoginPage(driver)
        login_page.goto()
        login_page.institutional_login_button.click()
        institutional_login_page = InstitutionalLoginPage(driver, verify=True)
        assert len(institutional_login_page.dropdown_options) > 1

    @markers.core_functionality
    def test_orcid_login(self, driver):
        """Check that you arrive on the orcid login page.
        """
        login_page = LoginPage(driver)
        login_page.goto()
        login_page.orcid_login_button.click()

        # If user is logged out of ORCID, ORCID's Oauth service will use
        # redirect link before landing on ORCID sign in page
        WebDriverWait(driver, 10).until(EC.url_contains('https://orcid.org/signin'))

        # Oauth will redirect to callback url with "error" if anything goes wrong
        assert 'error' not in driver.current_url
