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
        utils.delete_user(self.user)

        super(TestTopNavigationBar, self).tearDown()

    def test_osf_home_drop_down(self):
        pass

    def test_nagivation_bar_link(self):
        pass

    def test_user_profile_menu(self):
        pass

    def test_log_out(self):
        pass