from utils import launch_driver
from pythosf import client

import settings

API_TOKEN = settings.USER_ONE_TOKEN
API_DOMAIN = settings.API_DOMAIN

class SeleniumTest:

    @classmethod
    def setup_class(cls):
        cls.driver = launch_driver()
        cls.session = client.Session(api_base_url=API_DOMAIN, token=API_TOKEN)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
