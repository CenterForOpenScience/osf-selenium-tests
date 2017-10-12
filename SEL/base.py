import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wait

import settings
import utils


class SmokeTest(unittest.TestCase):
    """Base class for smoke tests. Creates a WebDriver
    on setUp and quits on tearDown.

    """
    # Allow multiprocessing for individual tests
    _multiprocess_can_split_ = True

    def setUp(self):

        # Launch Selenium using options specified as class
        # variables, which can include driver_name and
        # desired_capabilities
        if hasattr(self, 'driver_opts'):
            self.driver = utils.launch_driver(**self.driver_opts)
        else:
            self.driver = utils.launch_driver()

        self.site_root = settings.osf_home.strip('/')

    def tearDown(self):

        # Quit Selenium
        # Note: Use WebDriver.quit() instead of WebDriver.close();
        # otherwise, SauceLabs tests will never finish
        self.driver.quit()

    def get_element(self, css):
        return wait(
            driver=self.driver,
            timeout=5
        ).until(
            method=ec.visibility_of_element_located(
                (By.CSS_SELECTOR, css)
            )
        )