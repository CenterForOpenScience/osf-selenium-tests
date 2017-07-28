from Login import Login
import pytest
import time
from selenium import webdriver


@pytest.yield_fixture
def driver():
    desired_cap= {'browser': 'Chrome', 'browser_version': '59.0', 'os': 'Windows', 'os_version': '10', 'resolution': '1024x768'}
    driver= webdriver.Remote(
    command_executor='http://shikhadubey1:Mhtt1XkQq18k8nqQzsqn@hub.browserstack.com:80/wd/hub',
    desired_capabilities= desired_cap)
    yield driver
    driver.quit()
    
def test_login(driver):
  Login(driver)
