import pytest
import settings

from utils import launch_driver, logout
from pages.base import OSFBasePage, login
from pages.preprint import PreprintPage
from pages.meeting import MeetingPage
from pages.registries import RegistriesPage


class TestBasePageNavBar:

    @classmethod
    def setup_class(cls):
        cls.driver = launch_driver()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    def setup_method(self, method):
        self.base_page = OSFBasePage(self.driver)

    def teardown_method(self, method):
        logout(self.base_page)

    def test_osf_home_drop_down_home_link(self):
        self.base_page.navbar.service_dropdown.click()
        self.base_page.navbar.home_link.click()
        assert settings.OSF_HOME in self.driver.current_url

    def test_osf_home_drop_down_preprints_link(self):
        self.base_page.navbar.service_dropdown.click()
        self.base_page.navbar.preprints_link.click()
        preprints_url = settings.OSF_HOME + '/preprints/'
        assert self.driver.current_url == preprints_url

    def test_osf_home_drop_down_registries_link(self):
        self.base_page.navbar.service_dropdown.click()
        self.base_page.navbar.registries_link.click()
        registries_url = settings.OSF_HOME + '/registries/'
        assert self.driver.current_url == registries_url

    def test_osf_home_drop_down_meetings_link(self):
        self.base_page.navbar.service_dropdown.click()
        self.base_page.navbar.meetings_link.click()
        meetings_url = settings.OSF_HOME + '/meetings/'
        assert self.driver.current_url == meetings_url

    def test_nagivation_bar_link_my_projects_link_not_there_if_not_login(self):
        with pytest.raises(ValueError):
            self.base_page.navbar.my_project_link

    def test_nagivation_bar_link_my_projects_link_present_if_login(self):
        login(self.base_page)
        self.base_page.navbar.my_project_link.click()
        my_projects_url = settings.OSF_HOME + '/myprojects/'
        assert self.driver.current_url == my_projects_url

    def test_nagivation_bar_link_search_link(self):
        self.base_page.search_link.click()
        search_url = settings.OSF_HOME + '/search/'
        assert self.driver.current_url == search_url

    def test_nagivation_bar_link_support_link(self):
        self.base_page.support_link.click()
        support_url = settings.OSF_HOME + '/support/'
        assert self.driver.current_url == support_url

    def test_nagivation_bar_link_donate_link(self):
        self.base_page.donate_link.click()
        assert 'cos.io/donate-to-cos' in self.driver.current_url

    def test_user_dropdown_menu_not_there_if_not_login(self):
        with pytest.raises(ValueError):
            self.base_page.navbar.user_dropdown

    def test_user_profile_menu_profile_present_if_login(self):
        login(self.base_page)
        self.base_page.navbar.user_dropdown.click()
        self.base_page.navbar.user_dropdown_profile.click()
        profile_url = settings.OSF_HOME + '/profile/'
        assert self.driver.current_url == profile_url

    def test_user_profile_menu_support_present_if_login(self):
        login(self.base_page)
        self.base_page.navbar.user_dropdown.click()
        self.base_page.navbar.user_dropdown_support.click()
        support_url = settings.OSF_HOME + '/support/'
        assert self.driver.current_url == support_url

    def test_user_profile_menu_settings_present_if_login(self):
        login(self.base_page)
        self.base_page.navbar.user_dropdown.click()
        self.base_page.navbar.user_dropdown_settings.click()
        settings_url = settings.OSF_HOME + '/settings/'
        assert self.driver.current_url == settings_url

    def test_logout_link_present_if_login(self):
        login(self.base_page)
        self.base_page.navbar.user_dropdown.click()
        self.base_page.navbar.logout_link.click()
        assert 'goodbye' in self.driver.current_url

    def test_sign_in_button(self):
        self.base_page.navbar.sign_in_button.click()
        assert 'login' in self.driver.current_url

    def test_sign_in_button_not_present_if_login_in(self):
        login(self.base_page)
        with pytest.raises(ValueError):
            self.base_page.navbar.sign_in_button

    def test_sign_up_button(self):
        self.base_page.navbar.sign_up_button.click()
        assert 'register' in self.driver.current_url

    def test_sign_up_button_not_present_if_login_in(self):
        login(self.base_page)
        with pytest.raises(ValueError):
            self.base_page.navbar.sign_up_button


class TestPreprintsPageNavBar:

    @classmethod
    def setup_class(cls):
        cls.driver = launch_driver()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    def setup_method(self, method):
        self.preprint_page = PreprintPage(self.driver)

    def teardown_method(self, method):
        logout(self.preprint_page)

    def test_preprint_home_drop_down_home_link(self):
        self.preprint_page.navbar.service_dropdown.click()
        self.preprint_page.navbar.home_link.click()
        assert settings.OSF_HOME in self.driver.current_url

    def test_preprint_home_drop_down_preprints_link(self):
        self.preprint_page.navbar.service_dropdown.click()
        self.preprint_page.navbar.preprints_link.click()
        preprints_url = settings.OSF_HOME + '/preprints/'
        assert self.driver.current_url == preprints_url

    def test_preprint_home_drop_down_registries_link(self):
        self.preprint_page.navbar.service_dropdown.click()
        self.preprint_page.navbar.registries_link.click()
        registries_url = settings.OSF_HOME + '/registries/'
        assert self.driver.current_url == registries_url

    def test_preprint_home_drop_down_meetings_link(self):
        self.preprint_page.navbar.service_dropdown.click()
        self.preprint_page.navbar.meetings_link.click()
        meetings_url = settings.OSF_HOME + '/meetings/'
        assert self.driver.current_url == meetings_url

    def test_add_a_preprint_link_not_login(self):
        self.preprint_page.navbar.add_a_preprint_link.click()
        assert 'login' in self.driver.current_url

    def test_add_a_preprint_link_login(self):
        self.preprint_page.navbar.add_a_preprint_link.click()
        add_preprint_url = settings.OSF_HOME + '/preprints/submit/'
        assert self.driver.current_url == add_preprint_url

    def test_nagivation_bar_link_search_link(self):
        self.preprint_page.search_link.click()
        search_url = settings.OSF_HOME + '/search/'
        assert self.driver.current_url == search_url

    def test_nagivation_bar_link_support_link(self):
        self.preprint_page.support_link.click()
        support_url = settings.OSF_HOME + '/support/'
        assert self.driver.current_url == support_url

    def test_nagivation_bar_link_donate_link(self):
        self.preprint_page.donate_link.click()
        assert 'cos.io/donate-to-cos' in self.driver.current_url

    def test_user_dropdown_menu_not_there_if_not_login(self):
        with pytest.raises(ValueError):
            self.preprint_page.navbar.user_dropdown

    def test_user_profile_menu_profile_present_if_login(self):
        login(self.preprint_page)
        self.preprint_page.navbar.user_dropdown.click()
        self.preprint_page.navbar.user_dropdown_profile.click()
        profile_url = settings.OSF_HOME + '/profile/'
        assert self.driver.current_url == profile_url

    def test_user_profile_menu_support_present_if_login(self):
        login(self.preprint_page)
        self.preprint_page.navbar.user_dropdown.click()
        self.preprint_page.navbar.user_dropdown_support.click()
        support_url = settings.OSF_HOME + '/support/'
        assert self.driver.current_url == support_url

    def test_user_profile_menu_settings_present_if_login(self):
        login(self.preprint_page)
        self.preprint_page.navbar.user_dropdown.click()
        self.preprint_page.navbar.user_dropdown_settings.click()
        settings_url = settings.OSF_HOME + '/settings/'
        assert self.driver.current_url == settings_url

    def test_logout_link_present_if_login(self):
        login(self.preprint_page)
        self.preprint_page.navbar.user_dropdown.click()
        self.preprint_page.navbar.logout_link.click()
        assert 'goodbye' in self.driver.current_url

    def test_sign_in_button(self):
        self.preprint_page.navbar.sign_in_button.click()
        assert 'login' in self.driver.current_url

    def test_sign_in_button_not_present_if_login_in(self):
        login(self.preprint_page)
        with pytest.raises(ValueError):
            self.preprint_page.navbar.sign_in_button

    def test_sign_up_button(self):
        self.preprint_page.navbar.sign_up_button.click()
        assert 'register' in self.driver.current_url

    def test_sign_up_button_not_present_if_login_in(self):
        login(self.preprint_page)
        with pytest.raises(ValueError):
            self.preprint_page.navbar.sign_up_button


class TestMeetingPageNavBar:

    @classmethod
    def setup_class(cls):
        cls.driver = launch_driver()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    def setup_method(self, method):
        self.meeting_page = MeetingPage(self.driver)
        self.meeting_page.goto()

    def teardown_method(self, method):
        logout(self.meeting_page)

    def test_meeting_home_drop_down_home_link(self):
        self.meeting_page.navbar.service_dropdown.click()
        self.meeting_page.navbar.home_link.click()
        assert settings.OSF_HOME in self.driver.current_url

    def test_meeting_home_drop_down_preprints_link(self):
        self.meeting_page.navbar.service_dropdown.click()
        self.meeting_page.navbar.preprints_link.click()
        preprints_url = settings.OSF_HOME + '/preprints/'
        assert self.driver.current_url == preprints_url

    def test_meeting_home_drop_down_registries_link(self):
        self.meeting_page.navbar.service_dropdown.click()
        self.meeting_page.navbar.registries_link.click()
        registries_url = settings.OSF_HOME + '/registries/'
        assert self.driver.current_url == registries_url

    def test_meeting_home_drop_down_meetings_link(self):
        self.meeting_page.navbar.service_dropdown.click()
        self.meeting_page.navbar.meetings_link.click()
        meetings_url = settings.OSF_HOME + '/meetings/'
        assert self.driver.current_url == meetings_url

    def test_nagivation_bar_link_search_link_not_present(self):
        with pytest.raises(ValueError):
            self.meeting_page.search_link

    def test_nagivation_bar_link_support_link(self):
        self.meeting_page.support_link.click()
        support_url = settings.OSF_HOME + '/support/'
        assert self.driver.current_url == support_url

    def test_nagivation_bar_link_donate_link(self):
        self.meeting_page.donate_link.click()
        assert 'cos.io/donate-to-cos' in self.driver.current_url

    def test_user_dropdown_menu_not_there_if_not_login(self):
        with pytest.raises(ValueError):
            self.meeting_page.navbar.user_dropdown

    def test_user_profile_menu_profile_present_if_login(self):
        login(self.meeting_page)
        self.meeting_page.navbar.user_dropdown.click()
        self.meeting_page.navbar.user_dropdown_profile.click()
        profile_url = settings.OSF_HOME + '/profile/'
        assert self.driver.current_url == profile_url

    def test_user_profile_menu_support_present_if_login(self):
        login(self.meeting_page)
        self.meeting_page.navbar.user_dropdown.click()
        self.meeting_page.navbar.user_dropdown_support.click()
        support_url = settings.OSF_HOME + '/support/'
        assert self.driver.current_url == support_url

    def test_user_profile_menu_settings_present_if_login(self):
        login(self.meeting_page)
        self.meeting_page.navbar.user_dropdown.click()
        self.meeting_page.navbar.user_dropdown_settings.click()
        settings_url = settings.OSF_HOME + '/settings/'
        assert self.driver.current_url == settings_url

    def test_logout_link_present_if_login(self):
        login(self.meeting_page)
        self.meeting_page.navbar.user_dropdown.click()
        self.meeting_page.navbar.logout_link.click()
        assert 'goodbye' in self.driver.current_url

    def test_sign_in_button(self):
        self.meeting_page.navbar.sign_in_button.click()
        assert 'login' in self.driver.current_url

    def test_sign_in_button_not_present_if_login_in(self):
        login(self.meeting_page)
        with pytest.raises(ValueError):
            self.meeting_page.navbar.sign_in_button

    def test_sign_up_button(self):
        self.meeting_page.navbar.sign_up_button.click()
        assert 'register' in self.driver.current_url

    def test_sign_up_button_not_present_if_login_in(self):
        login(self.meeting_page)
        with pytest.raises(ValueError):
            self.meeting_page.navbar.sign_up_button


class TestRegistriesPageNavBar:

    @classmethod
    def setup_class(cls):
        cls.driver = launch_driver()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    def setup_method(self, method):
        self.registries_page = RegistriesPage(self.driver)

    def teardown_method(self, method):
        logout(self.registries_page)

    def test_registries_home_drop_down_home_link(self):
        self.registries_page.navbar.service_dropdown.click()
        self.registries_page.navbar.home_link.click()
        assert settings.OSF_HOME in self.driver.current_url

    def test_registries_home_drop_down_preprints_link(self):
        self.registries_page.navbar.service_dropdown.click()
        self.registries_page.navbar.preprints_link.click()
        preprints_url = settings.OSF_HOME + '/preprints/'
        assert self.driver.current_url == preprints_url

    def test_registries_home_drop_down_registries_link(self):
        self.registries_page.navbar.service_dropdown.click()
        self.registries_page.navbar.registries_link.click()
        registries_url = settings.OSF_HOME + '/registries/'
        assert self.driver.current_url == registries_url

    def test_registries_home_drop_down_meetings_link(self):
        self.registries_page.navbar.service_dropdown.click()
        self.registries_page.navbar.meetings_link.click()
        meetings_url = settings.OSF_HOME + '/meetings/'
        assert self.driver.current_url == meetings_url

    def test_nagivation_bar_link_search_link(self):
        self.registries_page.search_link.click()
        search_url = settings.OSF_HOME + '/search/'
        assert self.driver.current_url == search_url

    def test_nagivation_bar_link_support_link(self):
        self.registries_page.support_link.click()
        support_url = settings.OSF_HOME + '/support/'
        assert self.driver.current_url == support_url

    def test_nagivation_bar_link_donate_link(self):
        self.registries_page.donate_link.click()
        assert 'cos.io/donate-to-cos' in self.driver.current_url

    def test_user_dropdown_menu_not_there_if_not_login(self):
        with pytest.raises(ValueError):
            self.registries_page.navbar.user_dropdown

    def test_user_profile_menu_profile_present_if_login(self):
        login(self.registries_page)
        self.registries_page.navbar.user_dropdown.click()
        self.registries_page.navbar.user_dropdown_profile.click()
        profile_url = settings.OSF_HOME + '/profile/'
        assert self.driver.current_url == profile_url

    def test_user_profile_menu_support_present_if_login(self):
        login(self.registries_page)
        self.registries_page.navbar.user_dropdown.click()
        self.registries_page.navbar.user_dropdown_support.click()
        support_url = settings.OSF_HOME + '/support/'
        assert self.driver.current_url == support_url

    def test_user_profile_menu_settings_present_if_login(self):
        login(self.registries_page)
        self.registries_page.navbar.user_dropdown.click()
        self.registries_page.navbar.user_dropdown_settings.click()
        settings_url = settings.OSF_HOME + '/settings/'
        assert self.driver.current_url == settings_url

    def test_logout_link_present_if_login(self):
        login(self.registries_page)
        self.registries_page.navbar.user_dropdown.click()
        self.registries_page.navbar.logout_link.click()
        assert 'goodbye' in self.driver.current_url

    def test_sign_in_button(self):
        self.registries_page.navbar.sign_in_button.click()
        assert 'login' in self.driver.current_url

    def test_sign_in_button_not_present_if_login_in(self):
        login(self.registries_page)
        with pytest.raises(ValueError):
            self.registries_page.navbar.sign_in_button

    def test_sign_up_button(self):
        self.registries_page.navbar.sign_up_button.click()
        assert 'register' in self.driver.current_url

    def test_sign_up_button_not_present_if_login_in(self):
        login(self.registries_page)
        with pytest.raises(ValueError):
            self.registries_page.navbar.sign_up_button
