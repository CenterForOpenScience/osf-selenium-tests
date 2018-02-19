from pythosf import client

import settings
from utils import launch_driver

from pages.base import login
from pages.landing import LandingPage

API_DOMAIN = settings.API_DOMAIN
API_TOKEN = settings.USER_ONE_TOKEN

class SeleniumTest:

    @classmethod
    def setup_class(cls):
        cls.driver = launch_driver()
        cls.session = client.Session(api_base_url=API_DOMAIN, token=API_TOKEN)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    def assert_on_page(self, page_class):
        page_class(self.driver, verify=True)


class LoggedInTest(SeleniumTest):

    @classmethod
    def setup_class(cls):
        super(LoggedInTest, cls).setup_class()
        page = LandingPage(cls.driver)
        page.goto()
        login(page)
