import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from base import SmokeTest
import utils
import settings

driver = settings.DRIVER


class TestTopNavigationBar(SmokeTest):

    def setUp(self):
        super(TestTopNavigationBar, self).setUp()

        self.driver = utils.launch_driver()
        self.user = utils.create_user()

        utils.login(self.driver, self.user)
        self.driver.get(settings.osf_home)

    def tearDown(self):
        utils.logout(self.driver)
        utils.delete_user(self.user)

        super(TestTopNavigationBar, self).tearDown()

    def test_osf_home_drop_down_home(self):
        home_xpath = "//nav[@id='navbarScope']/div/div[@class='navbar-header']/" \
                           "div[@class='dropdown']/ul[@role='menu']/li/" \
                           "a[@href='" + settings.osf_home + "']"
        home = driver.find_element_by_xpath(
            home_xpath
        )
        assert home
        home.click()
        assert self.driver.current_url is settings.osf_home

    def test_osf_home_drop_down_preprints(self):
        preprints_url = settings.osf_home + '/preprints/'
        preprints_xpath = "//nav[@id='navbarScope']/div/div[@class='navbar-header']/" \
                     "div[@class='dropdown']/ul[@role='menu']/li/" \
                     "a[@href='" + preprints_url + "']"
        prerints = driver.find_element_by_xpath(
            preprints_xpath
        )
        assert prerints
        prerints.click()
        assert self.driver.current_url is preprints_url

    def test_osf_home_drop_down_registries(self):
        registries_url = settings.osf_home + '/registries/'
        registries_xpath = "//nav[@id='navbarScope']/div/div[@class='navbar-header']/" \
                          "div[@class='dropdown']/ul[@role='menu']/li/" \
                          "a[@href='" + registries_url + "']"
        registries = driver.find_element_by_xpath(
            registries_xpath
        )
        assert registries
        registries.click()
        assert self.driver.current_url is registries_url

    def test_osf_home_drop_down_meetings(self):
        meetings_url = settings.osf_home + '/meetings/'
        meetings_xpath = "//nav[@id='navbarScope']/div/div[@class='navbar-header']/" \
                           "div[@class='dropdown']/ul[@role='menu']/li/" \
                           "a[@href='" + meetings_url + "']"
        meetings = driver.find_element_by_xpath(
            meetings_xpath
        )
        assert meetings
        meetings.click()
        assert self.driver.current_url is meetings_url

    def test_nagivation_bar_link_my_projects(self):
        my_project_xpath = "//div[@id='secondary-navigation']/ul/li/a[@href='" + settings.osf_home + "/myprojects/']"
        my_projects = driver.find_element_by_xpath(
            my_project_xpath
        )
        assert my_projects
        my_projects.click()
        assert 'myprojects' in self.driver.current_url

    def test_nagivation_bar_link_search(self):
        search_xpath = "//div[@id='secondary-navigation']/ul/li/a[@href='" + settings.osf_home + "/search/']"
        search = driver.find_element_by_xpath(
            search_xpath
        )
        assert search
        search.click()
        assert 'myprojects' in self.driver.current_url

    def test_nagivation_bar_link_support(self):
        support = driver.find_element_by_xpath(
            "//div[@id='secondary-navigation']/ul/li/a[@href='/support/']"
        )
        assert support
        support.click()
        assert 'myprojects' in self.driver.current_url

    def test_nagivation_bar_link_donate(self):
        donate = driver.find_element_by_xpath(
            "//div[@id='secondary-navigation']/ul/li/a[@href='https://cos.io/donate']"
        )
        assert donate
        donate.click()
        assert 'cos.io/donate-to-cos' in self.driver.current_url

    def test_user_profile_menu_profile(self):
        profile = driver.find_element_by_xpath(
            "//div[@id='secondary-navigation']/ul/li[@class='dropdown']/ul/li/a[@href='/logout/']"
        )
        assert profile
        profile.click()
        assert 'profile' in self.driver.current_url

    def test_user_profile_menu_support(self):
        support = driver.find_element_by_xpath(
            "//div[@id='secondary-navigation']/ul/li[@class='dropdown']/ul/li/a[@href='https://osf.io/support/']"
        )
        assert support
        support.click()
        assert 'osf.io/support' in self.driver.current_url

    def test_user_profile_menu_settings(self):
        profile_settings = driver.find_element_by_xpath(
            "//div[@id='secondary-navigation']/ul/li[@class='dropdown']/ul/li/a[@href='/settings/']"
        )
        assert profile_settings
        profile_settings.click()
        assert 'settings' in self.driver.current_url

    def test_log_out(self):
        utils.logout(self.driver)
        assert 'goodbye' in self.driver.current_url