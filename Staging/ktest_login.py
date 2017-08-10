import pytest
from Blocks import Login
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def test_login():
	desired_cap = {'browser': 'Chrome', 'browser_version': '59.0', 'os': 'OS X', 'os_version': 'Sierra', 'resolution': '1920x1080'}

	driver = webdriver.Remote(
    	command_executor='http://patrickanderson2:Z39oMKMLFiyYJ88GWosk@hub.browserstack.com:80/wd/hub',
    	desired_capabilities=desired_cap)

	Login.staging_login(self, driver)
	assert driver.find_element_by_xpath("//*[@id='osfHome']/div[3]/div/div/div/div/div[1]/h2")
