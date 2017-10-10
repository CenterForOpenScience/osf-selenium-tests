import os
import settings
from helpers import login
from helpers import forks
from helpers import nodes
from helpers import meetings
from helpers import search

#driver = DRIVER
driver = settings.DRIVER
#DRIVER= webdriver.Remote(command_executor, desired_capabilities=DESIRED_CAP)

def test_meetings():
    #login.login(driver)
    driver.get("https://staging.osf.io/meetings/")
    time.sleep(3)
    driver.find_element_by_css_selector("#primary-navigation > span").click()
    time.sleep(2)
    driver.find_element_by_css_selector("#navbarScope > div > div.navbar-header > div.dropdown.primary-nav.open > ul > li:nth-child(1) > a > b").click()
    assert "https://staging.osf.io/" in driver.current_url
    time.sleep(3)
    driver.find_element_by_css_selector("#primary-navigation > span").click()
    time.sleep(1)
    driver.find_element_by_css_selector("#navbarScope > div > div.navbar-header > div.dropdown.primary-nav.open > ul > li:nth-child(2) > a > b").click()
    assert "https://staging.osf.io/preprints/" in driver.current_url
    time.sleep(2)
    driver.back() 
    time.sleep(3)
    driver.find_element_by_css_selector("#primary-navigation > span").click()
    driver.find_element_by_css_selector("#navbarScope > div > div.navbar-header > div.dropdown.primary-nav.open > ul > li:nth-child(3) > a > b").click()
    assert "https://staging.osf.io/registries/" in driver.current_url
    time.sleep(2)
    driver.back()
    time.sleep(2)
    driver.find_element_by_css_selector("#primary-navigation > span").click()
    driver.find_element_by_css_selector("#navbarScope > div > div.navbar-header > div.dropdown.primary-nav.open > ul > li:nth-child(4) > a > b").click()
    assert "https://staging.osf.io/meetings" in driver.current_url
    time.sleep(2)
    driver.back()

