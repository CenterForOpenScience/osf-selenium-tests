import pytest
import markers

from pages.login import LoginPage, login
from pages.cos import COSDonatePage
from pages.search import SearchPage
from pages.landing import LandingPage
from pages.support import SupportPage
from pages.meetings import MeetingsPage
from pages.register import RegisterPage
from pages.project import MyProjectsPage
from pages.dashboard import DashboardPage
from pages.registries import RegistriesLandingPage
from pages.user import UserProfilePage, ProfileInformationPage
from pages.preprints import PreprintLandingPage, PreprintSubmitPage
from pages.quickfiles import QuickfilesPage


# TODO: Test Navbar from all services including reviews and such - they might not have the same navbar always

class NavbarTestLoggedOutMixin:
    """Mixin used to inject generic tests
    """
    @pytest.fixture()
    def page(self, driver):
        raise NotImplementedError()

    def test_osf_home_dropdown_link(self, page, driver):
        page.navbar.service_dropdown.click()
        page.navbar.home_link.click()
        LandingPage(driver, verify=True)

    def test_preprints_dropdown_link(self, page, driver):
        page.navbar.service_dropdown.click()
        page.navbar.preprints_link.click()
        PreprintLandingPage(driver, verify=True)

    def test_registries_dropdown_link(self, driver, page):
        page.navbar.service_dropdown.click()
        page.navbar.registries_link.click()
        RegistriesLandingPage(driver, verify=True)

    def test_meetings_dropdown_link(self, page, driver):
        page.navbar.service_dropdown.click()
        page.navbar.meetings_link.click()
        MeetingsPage(driver, verify=True)

    def test_sign_up_button(self, driver, page):
        page.navbar.sign_up_button.click()
        RegisterPage(driver, verify=True)

    def test_user_dropdown_not_present(self, page):
        assert page.navbar.user_dropdown.absent()


# Class used to inject generic tests
class NavbarTestLoggedInMixin:
    """Mixin used to inject generic tests
    """
    @pytest.fixture()
    def page(self, driver):
        raise NotImplementedError()

    def test_user_profile_menu_profile_link(self, driver, page):
        page.navbar.user_dropdown.click()
        page.navbar.user_dropdown_profile.click()
        assert UserProfilePage(driver, verify=True)

    def test_user_profile_menu_support_link(self, driver, page):
        page.navbar.user_dropdown.click()
        page.navbar.user_dropdown_support.click()
        assert SupportPage(driver, verify=True)

    def test_user_profile_menu_settings_link(self, driver, page):
        page.navbar.user_dropdown.click()
        page.navbar.user_dropdown_settings.click()
        assert ProfileInformationPage(driver, verify=True)

    def test_sign_in_button_not_present(self, page):
        assert page.navbar.sign_in_button.absent()

    def test_sign_up_button_not_present(self, page):
        assert page.navbar.sign_up_button.absent()

    def test_logout_link(self, driver, page):
        page.navbar.user_dropdown.click()
        page.navbar.logout_link.click()
        LandingPage(driver, verify=True)
        assert 'goodbye' in driver.current_url
        login(driver)


class TestOSFHomeNavbar(NavbarTestLoggedOutMixin):

    @pytest.fixture()
    def page(self, driver):
        page = LandingPage(driver)
        page.goto()
        return page

    @markers.smoke_test
    @markers.core_functionality
    def test_my_projects_link_not_present(self, page):
        """Used as a core test to make sure the landing page loads.
        """
        assert page.navbar.my_projects_link.absent()

    def test_search_link(self, driver, page):
        page.navbar.search_link.click()
        assert SearchPage(driver, verify=True)

    @markers.smoke_test
    @markers.core_functionality
    def test_support_link(self, page, driver):
        """Used as a core test to make sure the support page loads.
        """
        page.navbar.support_link.click()
        assert SupportPage(driver, verify=True)

    def test_donate_link(self, page, driver):
        page.navbar.donate_link.click()
        donate_page = COSDonatePage(driver, verify=False)
        assert_donate_page(driver, donate_page)

    def test_sign_in_button(self, page, driver):
        page.navbar.sign_in_button.click()
        LoginPage(driver, verify=True)


class TestOSFHomeNavbarLoggedIn(NavbarTestLoggedInMixin):

    # Profile settings page
    @pytest.fixture()
    def page(self, driver, must_be_logged_in):
        page = DashboardPage(driver)
        page.goto()
        return page

    def test_my_projects_link(self, page, driver):
        page.navbar.my_projects_link.click()
        assert MyProjectsPage(driver, verify=True)

    def test_my_quick_files_link(self, page, driver):
        page.navbar.my_quick_files_link.click()
        QuickfilesPage(driver, verify=True)


# TODO: Complete this test after ENG-1103 is resolved
# class TestPreprintsNavbar(NavbarTestLoggedOutMixin):
#
#     @pytest.fixture()
#     def page(self, driver):
#         page = PreprintLandingPage(driver)
#         page.goto()
#         return page

    # todo: add id to those html tags in ember osf to make the find_element possible
    # def test_search_link(self):
    #     page.navbar.search_link.click()
    #     search_url = settings.OSF_HOME + '/search/'
    #     assert driver.current_url == search_url
    #
    # def test_support_link(self):
    #     page.navbar.support_link.click()
    #     support_url = settings.OSF_HOME + '/support/'
    #     assert driver.current_url == support_url
    #
    # def test_donate_link(self):
    #     page.navbar.donate_link.click()
    #     assert 'cos.io/donate-to-cos' in driver.current_url
    #
    # def test_sign_in_button(self):
    #     page.navbar.sign_in_button.click()
    #     assert 'login' in driver.current_url


@pytest.mark.usefixtures('must_be_logged_in')
class TestPreprintsNavbarLoggedIn(NavbarTestLoggedInMixin):

    @pytest.fixture()
    def page(self, driver):
        page = PreprintLandingPage(driver)
        page.goto()
        return page

    def test_add_a_preprint_link(self, page, driver):
        page.navbar.add_a_preprint_link.click()
        PreprintSubmitPage(driver, verify=True)


class TestMeetingsNavbar(NavbarTestLoggedOutMixin):

    @pytest.fixture()
    def page(self, driver):
        page = MeetingsPage(driver)
        page.goto()
        return page

    def test_support_link(self, page, driver):
        page.navbar.support_link.click()
        assert '360001550933' in driver.current_url or 'support' in driver.current_url

        # For future use
        # support_url = 'https://openscience.zendesk.com/hc/en-us/categories/360001550933'
        # assert driver.current_url == support_url

    def test_donate_link(self, page, driver):
        page.navbar.donate_link.click()
        donate_page = COSDonatePage(driver, verify=False)
        assert_donate_page(driver, donate_page)

    def test_sign_in_button(self, page, driver):
        page.navbar.sign_in_button.click()
        assert 'login' in driver.current_url


@pytest.mark.usefixtures('must_be_logged_in')
class TestMeetingsNavbarLoggedIn(NavbarTestLoggedInMixin):

    @pytest.fixture()
    def page(self, driver):
        page = MeetingsPage(driver)
        page.goto()
        return page


class TestRegistriesNavbar(NavbarTestLoggedOutMixin):

    @pytest.fixture()
    def page(self, driver):
        page = RegistriesLandingPage(driver)
        page.goto()
        return page

    # todo: add id to those html tags in ember osf to make the find_element possible
    # def test_search_link(self):
    #     page.navbar.search_link.click()
    #     search_url = settings.OSF_HOME + '/search/'
    #     assert driver.current_url == search_url
    #
    # def test_support_link(self):
    #     page.navbar.support_link.click()
    #     support_url = settings.OSF_HOME + '/support/'
    #     assert driver.current_url == support_url
    #
    # def test_donate_link(self):
    #     page.navbar.donate_link.click()
    #     assert 'cos.io/donate-to-cos' in driver.current_url
    #
    # def test_sign_in_button(self):
    #     page.navbar.sign_in_button.click()
    #     assert 'login' in driver.current_url


@pytest.mark.usefixtures('must_be_logged_in')
class TestRegistriesNavbarLoggedIn(NavbarTestLoggedInMixin):

    @pytest.fixture()
    def page(self, driver):
        page = RegistriesLandingPage(driver)
        page.goto()
        return page


def assert_donate_page(driver, donate_page):
    # locators.py does not currently support invisible elements as identity
    # https://github.com/cos-qa/osf-selenium-tests/blob/b7f3f21376b7d6f751993cdcffea9262856263e3/base/locators.py#L151
    meta_tag = driver.find_element_by_xpath('//meta[@name="cos:id" and @content="donate-page"]')

    assert driver.current_url == donate_page.url
    assert meta_tag.get_attribute('name') == 'cos:id'
    assert meta_tag.get_attribute('content') == 'donate-page'
