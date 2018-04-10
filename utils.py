import os

import settings
from base import expected_conditions as ec

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait


HERE = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

def launch_driver(driver_name=settings.DRIVER, desired_capabilities=None):
    """Create and configure a WebDriver.

    Args:
        driver_name : Name of WebDriver to use
        desired_capabilities : Desired browser specs

    """

    try:
        driver_cls = getattr(webdriver, driver_name)
    except AttributeError:
        driver_cls = getattr(webdriver, settings.DRIVER)

    if driver_name == 'Remote':
        if desired_capabilities is None:
            desired_capabilities = settings.DESIRED_CAP
        command_executor = 'http://{}:{}@hub.browserstack.com:80/wd/hub'.format(
            settings.BSTACK_USER,
            settings.BSTACK_KEY
        )
        driver = driver_cls(
            command_executor=command_executor,
            desired_capabilities=desired_capabilities
        )
        driver.maximize_window()
    elif driver_name == 'Chrome' and settings.HEADLESS:
        from webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('window-size=1200x600')
        driver = driver_cls(chrome_options=chrome_options)
    else:
        driver = driver_cls()

    return driver

def switch_to_tab(driver, page_index, timeout=settings.QUICK_TIMEOUT):
    try:
        WebDriverWait(driver, timeout).until(
            ec.window_at_index(page_index)
        )
        driver.switch_to.window(driver.window_handles[page_index])
    except TimeoutException:
        raise ValueError('No tab open at index {}. {}'.format(page_index, driver.current_url)) from None
