import os

# Selenium imports
from selenium import webdriver

# Project imports
import settings


def launch_driver(
        driver_name=None,
        desired_capabilities={},
        wait_time=settings.selenium_wait_time):
    """Create and configure a WebDriver.

    Args:
        driver_name : Name of WebDriver to use
        wait_time : Time to implicitly wait for element load

    """

    driver_name = driver_name or settings.driver_name

    driver_cls = getattr(webdriver, driver_name)

    if driver_name == 'Remote':

        # Set up command executor
        command_executor = 'http://%s:%s@ondemand.saucelabs.com:80/wd/hub' \
                           % (os.environ.get('SAUCE_USERNAME'), os.environ.get('SAUCE_ACCESS_KEY'))

        driver = driver_cls(
            desired_capabilities=desired_capabilities,
            command_executor=command_executor
        )
    else:

        driver = driver_cls()

    # Wait for elements to load
    driver.implicitly_wait(wait_time)

    # Return driver
    return driver

#TODO use api to get the user info to form a test user which should have everything like a real osf user
def create_user():
    pass

#TODO user api to delete the user after the test is done.
def delete_user(user):
    pass


def login(driver, user):
    