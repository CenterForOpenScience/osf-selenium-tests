import markers

from pages.login import LoginPage, InstitutionalLoginPage, OrcidLoginPage

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
    def test__orcid_login(self, driver):
        """Check that you arrive on the orcid login page.
        """
        login_page = LoginPage(driver)
        login_page.goto()
        login_page.orcid_login_button.click()
        OrcidLoginPage(driver, verify=True)
