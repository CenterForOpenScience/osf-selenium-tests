import os

# Selenium imports
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

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


find_btn = lambda elm: elm.find_element_by_xpath('.//button')


def fill_form(
        root,
        fields,
        button_finder=find_btn):
    """Fill out form fields and click submit button.

    Args:
        form : root element
        fields : dict of id -> value pairs for form
        button_finder : function to get button from root element

    """
    # Enter field values
    for field in fields:
        root.find_element_by_css_selector(field).send_keys(fields[field])

    # Click submit button
    button_finder(root).click()


def login(driver, user):
    driver.get(settings.osf_login_page)
    login_form = driver.find_element_by_id('fm1')

    fill_form(
        login_form,
        {
            '#username': user['username'],
            '#password': user['password'],
        }
    )


def logout(driver):
    """ Log out of OSF.

    Args:
        driver : selenium.webdriver instance

    """

    # locate and click logout button
    try:
        driver.find_element_by_xpath(
            "//div[@id='secondary-navigation']/ul/li[@class='dropdown']/ul/li/a[@href='/logout/']"
        ).click()
    except NoSuchElementException:
        # There is no logout link - assume the user is not logged in
        pass
