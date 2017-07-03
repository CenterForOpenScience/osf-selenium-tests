'''
Created on Jun 16, 2017

@author: patrickanderson
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

desired_cap = {'browser': 'Chrome', 'browser_version': '59.0', 'os': 'OS X', 'os_version': 'Sierra', 'resolution': '1920x1080'}

driver = webdriver.Remote(
    command_executor='http://patrickanderson2:Z39oMKMLFiyYJ88GWosk@hub.browserstack.com:80/wd/hub',
    desired_capabilities=desired_cap)

driver.get("http://www.google.com")
if not "Google" in driver.title:
    raise Exception("Unable to load google page!")
elem = driver.find_element_by_name("q")
elem.send_keys("BrowserStack")
elem.submit()
print driver.title
driver.quit()