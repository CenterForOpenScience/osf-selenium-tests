from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

desired_cap = {'browser': 'Firefox', 'browser_version': '53.0', 'os': 'OS X', 'os_version': 'El Capitan', 'resolution': '1024x768'}

driver = webdriver.Remote(
  command_executor='http://amandacos1:mvVRhGj3TDkmxLfKaXUT@hub.browserstack.com:80/wd/hub',
  desired_capabilities=desired_cap)

driver.get("http://www.google.com")
if not "Google" in driver.title:
    raise Exception("Unable to load google page!")
elem = driver.find_element_by_name("q")
elem.send_keys("BrowserStack")
elem.submit()
print driver.title
driver.quit()