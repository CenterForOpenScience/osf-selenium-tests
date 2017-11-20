import os

import settings
from selenium import webdriver


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
            os.environ.get('BSTACK_USER'),
            os.environ.get('BSTACK_KEY')
        )
        driver = driver_cls(
            command_executor=command_executor,
            desired_capabilities=desired_capabilities
        )

        # Maximize window to prevent visibility issues due to responsive design
        if desired_capabilities.get('browser') == 'Safari':
            driver.maximize_window()
        else:
            driver.set_window_size(1200, 720)
    elif driver_name == 'Chrome' and settings.HEADLESS:
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('window-size=1200x600')
        driver = driver_cls(chrome_options=chrome_options)
    else:
        driver = driver_cls()

    # Return driver
    return driver


def logout(osf_page):
    if osf_page.is_logged_in():
        osf_page.navbar.user_dropdown.click()
        osf_page.navbar.logout_link.click()
