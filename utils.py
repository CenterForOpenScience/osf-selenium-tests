import datetime
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

import settings


def launch_driver(driver_name=settings.DRIVER, desired_capabilities=None):
    """Create and configure a WebDriver for local or remote (BrowserStack) runs."""

    driver = None

    if driver_name == 'Remote':
        # Set BrowserStack capabilities
        if desired_capabilities is None:
            desired_capabilities = settings.DESIRED_CAP
        command_executor = 'http://{}:{}@hub.browserstack.com:80/wd/hub'.format(
            settings.BSTACK_USER, settings.BSTACK_KEY
        )

        browser = settings.BUILD.lower()

        if browser == 'firefox':
            ffo = FirefoxOptions()
            # Set custom user agent via capabilities (not by launching a local browser)
            desired_capabilities['browserName'] = 'Firefox'
            desired_capabilities['os'] = 'Windows'
            desired_capabilities['osVersion'] = '11'
            desired_capabilities['moz:firefoxOptions'] = {
                'prefs': {'general.useragent.override': 'OSF Selenium Bot'}
            }
            driver = webdriver.Remote(
                command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                options=ffo,
            )

        elif browser == 'chrome':
            chrome_options = ChromeOptions()
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('window-size=1200x600')
            chrome_options.add_argument(f'user-agent={"OSF Selenium Bot"}')
            desired_capabilities['browserName'] = 'Chrome'
            desired_capabilities['os'] = 'Windows'
            desired_capabilities['osVersion'] = '11'
            desired_capabilities['goog:chromeOptions'] = {
                'args': chrome_options.arguments
            }
            driver = webdriver.Remote(
                command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                options=chrome_options,
            )

        elif browser == 'edge':
            edge_options = EdgeOptions()
            desired_capabilities['browserName'] = 'Edge'
            desired_capabilities['os'] = 'Windows'
            desired_capabilities['osVersion'] = '11'
            driver = webdriver.Remote(
                command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                options=edge_options,
            )

        else:
            raise ValueError(f'Unsupported browser: {browser}')

    # Local browser launches below (for local development)
    elif driver_name == 'Chrome' and settings.HEADLESS:
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('window-size=1200x600')
        driver = webdriver.Chrome(options=chrome_options)

    elif driver_name == 'Chrome' and not settings.HEADLESS:
        chrome_options = ChromeOptions()
        preferences = {'download.default_directory': ''}
        chrome_options.add_experimental_option('prefs', preferences)
        driver = webdriver.Chrome(options=chrome_options)

    elif driver_name == 'Firefox':
        ffo = FirefoxOptions()
        ffo.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        driver = webdriver.Firefox(options=ffo)

    elif driver_name == 'Edge':
        edge_options = EdgeOptions()
        driver = webdriver.Edge(options=edge_options)
    else:
        driver = getattr(webdriver, driver_name)()

    if driver is None:
        raise RuntimeError(
            'WebDriver could not be instantiated based on provided configuration.'
        )

    driver.maximize_window()
    return driver


def find_current_browser(driver):
    current_browser = driver.desired_capabilities.get('browserName')
    return current_browser


def switch_to_new_tab(driver):
    # Took this snippet from browserstack support docs
    # https://www.browserstack.com/guide/how-to-switch-tabs-in-selenium-python

    # get current window handle
    main_window = driver.current_window_handle
    # get first child window
    all_windows = driver.window_handles
    for new_tab in all_windows:
        # switch focus to child window
        if new_tab != main_window:
            driver.switch_to.window(new_tab)
    # We need to return the main_window so we can keep track
    # of it and when we close the newly opened tab
    return main_window


def close_current_tab(driver, main_window):
    # close browser tab window
    driver.close()
    # switch to parent window
    driver.switch_to.window(main_window)


def find_row_by_name(files_page, file_name):
    all_files = files_page.file_rows
    for file_row in all_files:
        if file_name in file_row.text:
            return file_row
    return


def verify_file_download(driver, file_name):
    """Helper function to verify the file download functionality on the Project Files
    page.
    """

    current_date = datetime.datetime.now()
    if settings.DRIVER == 'Remote':
        # First verify the downloaded file exists on the virtual remote machine
        assert driver.execute_script(
            'browserstack_executor: {"action": "fileExists", "arguments": {"fileName": "%s"}}'
            % (file_name)
        )
        # Next get the file properties and then verify that the file creation date is today
        file_props = driver.execute_script(
            'browserstack_executor: {"action": "getFileProperties", "arguments": {"fileName": "%s"}}'
            % (file_name)
        )
        file_create_date = datetime.datetime.fromtimestamp(file_props['created_time'])
        assert file_create_date.date() == current_date.date()
    else:
        # First verify the downloaded file exists
        file_path = os.path.expanduser('~/Downloads/' + file_name)
        assert os.path.exists(file_path)
        # Next verify the file was downloaded today
        file_mtime = os.path.getmtime(file_path)
        file_mod_date = datetime.datetime.fromtimestamp(file_mtime)
        assert file_mod_date.date() == current_date.date()


def latest_download_file():
    path = os.path.expanduser('~/Downloads/')
    os.chdir(path)
    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    newest = files[-1]
    return newest


def get_guid_from_url(url, itemno):
    url_string_list = url.split('/')
    guid = url_string_list[itemno]
    return guid


def read_data_from_table(driver, table_path, check_match, item_match=None):
    datalist = []
    table_data = driver.find_element_by_xpath(table_path)
    path1 = table_path + '/tbody/tr'
    rows = table_data.find_elements_by_xpath(path1)
    rlen = len(rows)

    for i in range(1, rlen + 1):
        path2 = path1 + '[' + str(i) + ']/td'
        items = driver.find_elements_by_xpath(path2)
        clen = len(items)
        for j in range(1, clen + 1):
            path3 = path2 + '[' + str(j) + ']'
            cell_data = driver.find_element_by_xpath(path3).text
            datalist.append(cell_data)
            if check_match:
                if item_match in cell_data:
                    return i, datalist

    return rlen, datalist


def clean_text(stringvalue):
    clean_text = stringvalue.strip()
    clean_text = clean_text.replace('\n', ' ')
    clean_text = ' '.join(clean_text.split())
    return clean_text
