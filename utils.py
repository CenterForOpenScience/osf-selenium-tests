import os
import re
import time
import uuid

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

import settings


def launch_driver(
        driver_name=settings.DRIVER,
        desired_capabilities=None,
        wait_time=settings.SEL_WAIT):
    """Create and configure a WebDriver.

    Args:
        driver_name : Name of WebDriver to use
        wait_time : Time to implicitly wait for element load

    """

    try:
        driver_cls = getattr(webdriver, driver_name)
    except AttributeError:
        driver_cls = getattr(webdriver, settings.DRIVER)

    if driver_name == 'Remote':
        if desired_capabilities is None:
            desired_capabilities = settings.DESIRED_CAP
        command_executor = 'http://{}:{}@hub.browserstack.com:80/wd/hub'.format(
            os_env.get('BSTACK_USER'),
            os_env.get('BSTACK_KEY')
        )
        driver = driver_cls(
            command_executor=command_executor,
            desired_capabilities=desired_capabilities
        )
    elif driver_name == 'Chrome' and settings.HEADLESS:
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('window-size=1200x600')
        driver = driver_cls(chrome_options=chrome_options)
    else:
        driver = driver_cls()
        # Maximize window to prevent visibility issues due to responsive design
        driver.maximize_window()

    # Wait for elements to load
    driver.implicitly_wait(wait_time)

    # Return driver
    return driver
