import pytest
import settings

from utils import launch_driver, login
from pages.base import OSFBasePage
from pages.preprint import PreprintPage
from pages.meeting import MeetingPage
from pages.registries import RegistriesPage


class BasePageNavBarTests:

    @classmethod
    def setup_class(cls):
        cls.driver = launch_driver()

    def setup_method(self, method):
        self.base_page = OSFBasePage(self.driver)
        self.base_page.goto()

    def test_osf_home_drop_down_home(self):
        self.base_page.navbar.home.click()
        assert self.driver.current_url is settings.OSF_HOME

    def test_osf_home_drop_down_preprints(self):
        self.base_page.navbar.preprints.click()
        preprints_url = settings.OSF_HOME + '/preprints/'
        assert self.driver.current_url is preprints_url

    def test_osf_home_drop_down_registries(self):
        self.base_page.navbar.registries.click()
        registries_url = settings.OSF_HOME + '/registries/'
        assert self.driver.current_url is registries_url

    def test_osf_home_drop_down_meetings(self):
        self.base_page.navbar.meetings.click()
        meetings_url = settings.OSF_HOME + '/meetings/'
        assert self.driver.current_url is meetings_url

    def test_nagivation_bar_link_my_projects_not_there_if_not_login(self):
        assert len(self.base_page.navbar.my_project) == 0

    def test_nagivation_bar_link_my_projects_present_if_login(self):
        login(self.base_page)
        assert len(self.base_page.navbar.my_project) == 1
        self.base_page.navbar.my_project.click()
        my_projects_url = settings.OSF_HOME + '/myprojects/'
        assert self.driver.current_url is my_projects_url

    def test_nagivation_bar_link_search(self):
        self.base_page.search.click()
        search_url = settings.OSF_HOME + '/search/'
        assert self.driver.current_url is search_url

    def test_nagivation_bar_link_support(self):
        self.base_page.support.click()
        support_url = settings.OSF_HOME + '/support/'
        assert self.driver.current_url is support_url

    def test_nagivation_bar_link_donate(self):
        self.base_page.donate.click()
        assert 'cos.io/donate-to-cos' in self.driver.current_url

    def test_user_profile_menu_profile_not_there_if_not_login(self):
        assert len(self.base_page.navbar.user_dropdown_profile) == 0

    def test_user_profile_menu_profile_present_if_login(self):
        login(self.base_page)
        assert len(self.base_page.navbar.user_dropdown_profile) == 1
        self.base_page.navbar.user_dropdown_profile.click()
        profile_url = settings.OSF_HOME + '/profile/'
        assert self.driver.current_url is profile_url

    def test_user_profile_menu_support_not_there_if_not_login(self):
        assert len(self.base_page.navbar.user_dropdown_support) == 0

    def test_user_profile_menu_support_present_if_login(self):
        login(self.base_page)
        assert len(self.base_page.navbar.user_dropdown_support) == 1
        self.base_page.navbar.user_dropdown_support.click()
        support_url = settings.OSF_HOME + '/support/'
        assert self.driver.current_url is support_url

    def test_user_profile_menu_settings_not_there_if_not_login(self):
        assert len(self.base_page.navbar.user_dropdown_settings) == 0

    def test_user_profile_menu_settings_present_if_login(self):
        login(self.base_page)
        assert len(self.base_page.navbar.user_dropdown_settings) == 1
        self.base_page.navbar.user_dropdown_settings.click()
        settings_url = settings.OSF_HOME + '/settings/'
        assert self.driver.current_url is settings_url

    def test_logout_link_not_there_if_not_login(self):
        assert len(self.base_page.navbar.logout_link) == 0

    def test_logout_link_present_if_login(self):
        login(self.base_page)
        assert len(self.base_page.navbar.logout_link) == 1
        self.base_page.navbar.logout_link.click()
        assert 'goodbye' in self.driver.current_url

    def test_sign_in_button(self):
        assert len(self.base_page.navbar.sign_in_button) == 1
        self.base_page.navbar.sign_in_button.click()
        assert 'login' in self.driver.current_url

    def test_sign_in_button_not_present_if_login_in(self):
        login(self.base_page)
        assert len(self.base_page.navbar.sign_in_button) == 0

    def test_sign_up_button(self):
        assert len(self.base_page.navbar.sign_up_button) == 1
        self.base_page.navbar.sign_in_button.click()
        assert 'register' in self.driver.current_url

    def test_sign_up_button_not_present_if_login_in(self):
        login(self.base_page)
        assert len(self.base_page.navbar.sign_up_button) == 0

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()


class PreprintsPageNavBarTests:

    @classmethod
    def setup_class(cls):
        cls.driver = launch_driver()

    def setup_method(self, method):
        self.preprint_page = PreprintPage(self.driver)
        self.preprint_page.goto()

    def test_osf_home_drop_down_home(self):
        self.preprint_page.navbar.home.click()
        assert self.driver.current_url is settings.OSF_HOME

    def test_osf_home_drop_down_preprints(self):
        self.preprint_page.navbar.preprints.click()
        preprints_url = settings.OSF_HOME + '/preprints/'
        assert self.driver.current_url is preprints_url

    def test_osf_home_drop_down_registries(self):
        self.preprint_page.navbar.registries.click()
        registries_url = settings.OSF_HOME + '/registries/'
        assert self.driver.current_url is registries_url

    def test_osf_home_drop_down_meetings(self):
        self.preprint_page.navbar.meetings.click()
        meetings_url = settings.OSF_HOME + '/meetings/'
        assert self.driver.current_url is meetings_url

    def test_add_a_preprint_not_login(self):
        self.preprint_page.navbar.add_a_preprint.click()
        assert 'login' in self.driver.current_url

    def test_add_a_preprint_login(self):
        self.preprint_page.navbar.add_a_preprint.click()
        add_preprint_url = settings.OSF_HOME + '/preprints/submit/'
        assert self.driver.current_url is add_preprint_url

    def test_nagivation_bar_link_search(self):
        self.preprint_page.search.click()
        search_url = settings.OSF_HOME + '/search/'
        assert self.driver.current_url is search_url

    def test_nagivation_bar_link_support(self):
        self.preprint_page.support.click()
        support_url = settings.OSF_HOME + '/support/'
        assert self.driver.current_url is support_url

    def test_nagivation_bar_link_donate(self):
        self.preprint_page.donate.click()
        assert 'cos.io/donate-to-cos' in self.driver.current_url

    def test_user_profile_menu_profile_not_there_if_not_login(self):
        assert len(self.preprint_page.navbar.user_dropdown_profile) == 0

    def test_user_profile_menu_profile_present_if_login(self):
        login(self.preprint_page)
        assert len(self.preprint_page.navbar.user_dropdown_profile) == 1
        self.preprint_page.navbar.user_dropdown_profile.click()
        profile_url = settings.OSF_HOME + '/profile/'
        assert self.driver.current_url is profile_url

    def test_user_profile_menu_support_not_there_if_not_login(self):
        assert len(self.preprint_page.navbar.user_dropdown_support) == 0

    def test_user_profile_menu_support_present_if_login(self):
        login(self.preprint_page)
        assert len(self.preprint_page.navbar.user_dropdown_support) == 1
        self.preprint_page.navbar.user_dropdown_support.click()
        support_url = settings.OSF_HOME + '/support/'
        assert self.driver.current_url is support_url

    def test_user_profile_menu_settings_not_there_if_not_login(self):
        assert len(self.preprint_page.navbar.user_dropdown_settings) == 0

    def test_user_profile_menu_settings_present_if_login(self):
        login(self.preprint_page)
        assert len(self.preprint_page.navbar.user_dropdown_settings) == 1
        self.preprint_page.navbar.user_dropdown_settings.click()
        settings_url = settings.OSF_HOME + '/settings/'
        assert self.driver.current_url is settings_url

    def test_logout_link_not_there_if_not_login(self):
        assert len(self.preprint_page.navbar.logout_link) == 0

    def test_logout_link_present_if_login(self):
        login(self.preprint_page)
        assert len(self.preprint_page.navbar.logout_link) == 1
        self.preprint_page.navbar.logout_link.click()
        assert 'goodbye' in self.driver.current_url

    def test_sign_in_button(self):
        assert len(self.preprint_page.navbar.sign_in_button) == 1
        self.preprint_page.navbar.sign_in_button.click()
        assert 'login' in self.driver.current_url

    def test_sign_in_button_not_present_if_login_in(self):
        login(self.preprint_page)
        assert len(self.preprint_page.navbar.sign_in_button) == 0

    def test_sign_up_button(self):
        assert len(self.preprint_page.navbar.sign_up_button) == 1
        self.preprint_page.navbar.sign_in_button.click()
        assert 'register' in self.driver.current_url

    def test_sign_up_button_not_present_if_login_in(self):
        login(self.preprint_page)
        assert len(self.preprint_page.navbar.sign_up_button) == 0

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()


class MeetingPageNavBarTests:

    @classmethod
    def setup_class(cls):
        cls.driver = launch_driver()

    def setup_method(self, method):
        self.meeting_page = MeetingPage(self.driver)
        self.meeting_page.goto()

    def test_osf_home_drop_down_home(self):
        self.meeting_page.navbar.home.click()
        assert self.driver.current_url is settings.OSF_HOME

    def test_osf_home_drop_down_preprints(self):
        self.meeting_page.navbar.preprints.click()
        preprints_url = settings.OSF_HOME + '/preprints/'
        assert self.driver.current_url is preprints_url

    def test_osf_home_drop_down_registries(self):
        self.meeting_page.navbar.registries.click()
        registries_url = settings.OSF_HOME + '/registries/'
        assert self.driver.current_url is registries_url

    def test_osf_home_drop_down_meetings(self):
        self.meeting_page.navbar.meetings.click()
        meetings_url = settings.OSF_HOME + '/meetings/'
        assert self.driver.current_url is meetings_url

    def test_nagivation_bar_link_search(self):
        self.meeting_page.search.click()
        search_url = settings.OSF_HOME + '/search/'
        assert self.driver.current_url is search_url

    def test_nagivation_bar_link_support(self):
        self.meeting_page.support.click()
        support_url = settings.OSF_HOME + '/support/'
        assert self.driver.current_url is support_url

    def test_nagivation_bar_link_donate(self):
        self.meeting_page.donate.click()
        assert 'cos.io/donate-to-cos' in self.driver.current_url

    def test_user_profile_menu_profile_not_there_if_not_login(self):
        assert len(self.meeting_page.navbar.user_dropdown_profile) == 0

    def test_user_profile_menu_profile_present_if_login(self):
        login(self.meeting_page)
        assert len(self.meeting_page.navbar.user_dropdown_profile) == 1
        self.meeting_page.navbar.user_dropdown_profile.click()
        profile_url = settings.OSF_HOME + '/profile/'
        assert self.driver.current_url is profile_url

    def test_user_profile_menu_support_not_there_if_not_login(self):
        assert len(self.meeting_page.navbar.user_dropdown_support) == 0

    def test_user_profile_menu_support_present_if_login(self):
        login(self.meeting_page)
        assert len(self.meeting_page.navbar.user_dropdown_support) == 1
        self.meeting_page.navbar.user_dropdown_support.click()
        support_url = settings.OSF_HOME + '/support/'
        assert self.driver.current_url is support_url

    def test_user_profile_menu_settings_not_there_if_not_login(self):
        assert len(self.meeting_page.navbar.user_dropdown_settings) == 0

    def test_user_profile_menu_settings_present_if_login(self):
        login(self.meeting_page)
        assert len(self.meeting_page.navbar.user_dropdown_settings) == 1
        self.meeting_page.navbar.user_dropdown_settings.click()
        settings_url = settings.OSF_HOME + '/settings/'
        assert self.driver.current_url is settings_url

    def test_logout_link_not_there_if_not_login(self):
        assert len(self.meeting_page.navbar.logout_link) == 0

    def test_logout_link_present_if_login(self):
        login(self.meeting_page)
        assert len(self.meeting_page.navbar.logout_link) == 1
        self.meeting_page.navbar.logout_link.click()
        assert 'goodbye' in self.driver.current_url

    def test_sign_in_button(self):
        assert len(self.meeting_page.navbar.sign_in_button) == 1
        self.meeting_page.navbar.sign_in_button.click()
        assert 'login' in self.driver.current_url

    def test_sign_in_button_not_present_if_login_in(self):
        login(self.meeting_page)
        assert len(self.meeting_page.navbar.sign_in_button) == 0

    def test_sign_up_button(self):
        assert len(self.meeting_page.navbar.sign_up_button) == 1
        self.meeting_page.navbar.sign_in_button.click()
        assert 'register' in self.driver.current_url

    def test_sign_up_button_not_present_if_login_in(self):
        login(self.meeting_page)
        assert len(self.meeting_page.navbar.sign_up_button) == 0

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()


class RegistriesPageNavBarTests:

    @classmethod
    def setup_class(cls):
        cls.driver = launch_driver()

    def setup_method(self, method):
        self.registries_page = RegistriesPage(self.driver)
        self.registries_page.goto()

    def test_osf_home_drop_down_home(self):
        self.registries_page.navbar.home.click()
        assert self.driver.current_url is settings.OSF_HOME

    def test_osf_home_drop_down_preprints(self):
        self.registries_page.navbar.preprints.click()
        preprints_url = settings.OSF_HOME + '/preprints/'
        assert self.driver.current_url is preprints_url

    def test_osf_home_drop_down_registries(self):
        self.registries_page.navbar.registries.click()
        registries_url = settings.OSF_HOME + '/registries/'
        assert self.driver.current_url is registries_url

    def test_osf_home_drop_down_meetings(self):
        self.registries_page.navbar.meetings.click()
        meetings_url = settings.OSF_HOME + '/meetings/'
        assert self.driver.current_url is meetings_url

    def test_nagivation_bar_link_search(self):
        self.registries_page.search.click()
        search_url = settings.OSF_HOME + '/search/'
        assert self.driver.current_url is search_url

    def test_nagivation_bar_link_support(self):
        self.registries_page.support.click()
        support_url = settings.OSF_HOME + '/support/'
        assert self.driver.current_url is support_url

    def test_nagivation_bar_link_donate(self):
        self.registries_page.donate.click()
        assert 'cos.io/donate-to-cos' in self.driver.current_url

    def test_user_profile_menu_profile_not_there_if_not_login(self):
        assert len(self.registries_page.navbar.user_dropdown_profile) == 0

    def test_user_profile_menu_profile_present_if_login(self):
        login(self.registries_page)
        assert len(self.registries_page.navbar.user_dropdown_profile) == 1
        self.registries_page.navbar.user_dropdown_profile.click()
        profile_url = settings.OSF_HOME + '/profile/'
        assert self.driver.current_url is profile_url

    def test_user_profile_menu_support_not_there_if_not_login(self):
        assert len(self.registries_page.navbar.user_dropdown_support) == 0

    def test_user_profile_menu_support_present_if_login(self):
        login(self.registries_page)
        assert len(self.registries_page.navbar.user_dropdown_support) == 1
        self.registries_page.navbar.user_dropdown_support.click()
        support_url = settings.OSF_HOME + '/support/'
        assert self.driver.current_url is support_url

    def test_user_profile_menu_settings_not_there_if_not_login(self):
        assert len(self.registries_page.navbar.user_dropdown_settings) == 0

    def test_user_profile_menu_settings_present_if_login(self):
        login(self.registries_page)
        assert len(self.registries_page.navbar.user_dropdown_settings) == 1
        self.registries_page.navbar.user_dropdown_settings.click()
        settings_url = settings.OSF_HOME + '/settings/'
        assert self.driver.current_url is settings_url

    def test_logout_link_not_there_if_not_login(self):
        assert len(self.registries_page.navbar.logout_link) == 0

    def test_logout_link_present_if_login(self):
        login(self.registries_page)
        assert len(self.registries_page.navbar.logout_link) == 1
        self.registries_page.navbar.logout_link.click()
        assert 'goodbye' in self.driver.current_url

    def test_sign_in_button(self):
        assert len(self.registries_page.navbar.sign_in_button) == 1
        self.registries_page.navbar.sign_in_button.click()
        assert 'login' in self.driver.current_url

    def test_sign_in_button_not_present_if_login_in(self):
        login(self.registries_page)
        assert len(self.registries_page.navbar.sign_in_button) == 0

    def test_sign_up_button(self):
        assert len(self.registries_page.navbar.sign_up_button) == 1
        self.registries_page.navbar.sign_in_button.click()
        assert 'register' in self.driver.current_url

    def test_sign_up_button_not_present_if_login_in(self):
        login(self.registries_page)
        assert len(self.registries_page.navbar.sign_up_button) == 0

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()