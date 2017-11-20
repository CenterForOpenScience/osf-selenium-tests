from utils import launch_driver

class SeleniumTest:

    @classmethod
    def setup_class(cls):
        cls.driver = launch_driver()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
