import settings
from selenium import webdriver


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
    elif driver_name == 'Chrome' and settings.HEADLESS:
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('window-size=1200x600')
        # chrome_options.set_headless = True
        driver = driver_cls(chrome_options=chrome_options)
    elif driver_name == 'Chrome' and not settings.HEADLESS:
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.add_experimental_option('w3c', False)
        driver = driver_cls(chrome_options=chrome_options)
    elif driver_name == 'Firefox' and not settings.HEADLESS:
        global downloadDir
        downloadDir = ''

        from selenium.webdriver import FirefoxProfile
        fp = FirefoxProfile()
        fp.set_preference('browser.download.folderList', 2)
        fp.set_preference('browser.download.manager.showWhenStarting', False)
        fp.set_preference('browser.download.dir', downloadDir)
        fp.set_preference('browser.helperApps.neverAsk.saveToDisk',
                          'text/plain, application/octet-stream, application/binary, text/csv, application/csv, application/excel, text/comma-separated-values, text/xml, application/xml')
        driver = driver_cls(firefox_profile=fp)
    else:
        driver = driver_cls()

    driver.maximize_window()
    return driver
