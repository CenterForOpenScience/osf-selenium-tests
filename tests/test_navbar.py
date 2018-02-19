import settings

from pages.base import login
from pages.landing import LandingPage
from pages.meeting import MeetingPage
from pages.dashboard import DashboardPage
from pages.registries import RegistriesPage
from pages.preprint import PreprintPage, SubmitPreprintPage

from tests.base import SeleniumTest, LoggedInTest

#TODO: Test Navbar from all services including reviews and such - they might not have the same navbar always

class NavbarTestLoggedOut(SeleniumTest):

    def test_osf_home_dropdown_link(self):
        self.page.navbar.service_dropdown.click()
        self.page.navbar.home_link.click()
        self.assert_on_page(LandingPage)

    def test_preprints_dropdown_link(self):
        self.page.navbar.service_dropdown.click()
        self.page.navbar.preprints_link.click()
        self.assert_on_page(PreprintPage)

    def test_registries_dropdown_link(self):
        self.page.navbar.service_dropdown.click()
        self.page.navbar.registries_link.click()
        self.assert_on_page(RegistriesPage)

    def test_meetings_dropdown_link(self):
        self.page.navbar.service_dropdown.click()
        self.page.navbar.meetings_link.click()
        self.assert_on_page(MeetingPage)

    def test_sign_up_button(self):
        self.page.navbar.sign_up_button.click()
        assert 'register' in self.driver.current_url

    def test_user_dropdown_not_present(self):
        assert self.page.navbar.user_dropdown.absent()


class NavbarTestLoggedIn(LoggedInTest):

    def test_user_profile_menu_profile_link(self):
        self.page.navbar.user_dropdown.click()
        self.page.navbar.user_dropdown_profile.click()
        profile_url = settings.OSF_HOME + '/profile/'
        assert self.driver.current_url == profile_url

    def test_user_profile_menu_support_link(self):
        self.page.navbar.user_dropdown.click()
        self.page.navbar.user_dropdown_support.click()
        support_url = settings.OSF_HOME + '/support/'
        assert self.driver.current_url == support_url

    def test_user_profile_menu_settings_link(self):
        self.page.navbar.user_dropdown.click()
        self.page.navbar.user_dropdown_settings.click()
        settings_url = settings.OSF_HOME + '/settings/'
        assert self.driver.current_url == settings_url

    def test_sign_in_button_not_present(self):
        assert self.page.navbar.sign_in_button.absent()

    def test_sign_up_button_not_present(self):
        assert self.page.navbar.sign_up_button.absent()

    def test_logout_link(self):
        self.page.navbar.user_dropdown.click()
        self.page.navbar.logout_link.click()
        assert 'goodbye' in self.driver.current_url
        login(self.page)


class TestOSFHomeNavbar(NavbarTestLoggedOut):

    def setup_method(self, method):
        self.page = LandingPage(self.driver)
        self.page.goto()

    def test_my_projects_link_not_present(self):
        assert self.page.navbar.my_project_link.absent()

    def test_search_link(self):
        self.page.navbar.search_link.click()
        search_url = settings.OSF_HOME + '/search/'
        assert self.driver.current_url == search_url

    def test_support_link(self):
        self.page.navbar.support_link.click()
        support_url = settings.OSF_HOME + '/support/'
        assert self.driver.current_url == support_url

    def test_donate_link(self):
        self.page.navbar.donate_link.click()
        assert 'cos.io/donate-to-cos' in self.driver.current_url

    def test_sign_in_button(self):
        self.page.navbar.sign_in_button.click()
        assert 'login' in self.driver.current_url


class TestOSFHomeNavbarLoggedIn(NavbarTestLoggedIn):

    def setup_method(self, method):
        self.page = DashboardPage(self.driver)
        self.page.goto()

    def test_my_projects_link(self):
        self.page.navbar.my_project_link.click()
        my_projects_url = settings.OSF_HOME + '/myprojects/'
        assert self.driver.current_url == my_projects_url


class TestPreprintsNavbar(NavbarTestLoggedOut):

    def setup_method(self, method):
        self.page = PreprintPage(self.driver)
        self.page.goto()

    # todo: add id to those html tags in ember osf to make the find_element possible
    # def test_search_link(self):
    #     self.page.navbar.search_link.click()
    #     search_url = settings.OSF_HOME + '/search/'
    #     assert self.driver.current_url == search_url
    #
    # def test_support_link(self):
    #     self.page.navbar.support_link.click()
    #     support_url = settings.OSF_HOME + '/support/'
    #     assert self.driver.current_url == support_url
    #
    # def test_donate_link(self):
    #     self.page.navbar.donate_link.click()
    #     assert 'cos.io/donate-to-cos' in self.driver.current_url
    #
    # def test_sign_in_button(self):
    #     self.page.navbar.sign_in_button.click()
    #     assert 'login' in self.driver.current_url


class TestPreprintsNavbarLoggedIn(NavbarTestLoggedIn):

    def setup_method(self, method):
        self.page = PreprintPage(self.driver)
        self.page.goto()

    def test_add_a_preprint_link(self):
        self.page.navbar.add_a_preprint_link.click()
        self.assert_on_page(SubmitPreprintPage)


class TestMeetingsNavbar(NavbarTestLoggedOut):

    def setup_method(self, method):
        self.page = MeetingPage(self.driver)
        self.page.goto()

    def test_search_link_not_present(self):
        assert self.page.navbar.search_link.absent()

    def test_support_link(self):
        self.page.navbar.support_link.click()
        support_url = 'http://help.osf.io/m/meetings/'
        assert self.driver.current_url == support_url

    def test_donate_link(self):
        self.page.navbar.donate_link.click()
        assert 'cos.io/donate-to-cos' in self.driver.current_url

    def test_sign_in_button(self):
        self.page.navbar.sign_in_button.click()
        assert 'login' in self.driver.current_url


class TestMeetingsNavbarLoggedIn(NavbarTestLoggedIn):

    def setup_method(self, method):
        self.page = MeetingPage(self.driver)
        self.page.goto()


class TestRegistriesNavbar(NavbarTestLoggedOut):

    def setup_method(self, method):
        self.page = RegistriesPage(self.driver)
        self.page.goto()

    # todo: add id to those html tags in ember osf to make the find_element possible
    # def test_search_link(self):
    #     self.page.navbar.search_link.click()
    #     search_url = settings.OSF_HOME + '/search/'
    #     assert self.driver.current_url == search_url
    #
    # def test_support_link(self):
    #     self.page.navbar.support_link.click()
    #     support_url = settings.OSF_HOME + '/support/'
    #     assert self.driver.current_url == support_url
    #
    # def test_donate_link(self):
    #     self.page.navbar.donate_link.click()
    #     assert 'cos.io/donate-to-cos' in self.driver.current_url
    #
    # def test_sign_in_button(self):
    #     self.page.navbar.sign_in_button.click()
    #     assert 'login' in self.driver.current_url


class TestRegistriesNavbarLoggedIn(NavbarTestLoggedIn):

    def setup_method(self, method):
        self.page = RegistriesPage(self.driver)
        self.page.goto()
