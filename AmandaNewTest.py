
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from threading import Thread
import time#
from selenium.webdriver.support.select import Select
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

desired_cap = {'browser': 'Firefox', 'browser_version': '53.0', 'os': 'OS X', 'os_version': 'El Capitan', 'resolution': '1024x768'}

driver = webdriver.Remote(
command_executor='http://amandacos1:mvVRhGj3TDkmxLfKaXUT@hub.browserstack.com:80/wd/hub',
desired_capabilities=desired_cap)
driver.get("https://staging.osf.io/")
time.sleep(3)
driver.find_element_by_partial_link_text("Sign In").click()
time.sleep(3)
driver.find_element_by_id("username").send_keys("amanda@cos.io")
time.sleep(3)
driver.find_element_by_id('password').send_keys('CosWel@3i')
time.sleep(3)
driver.implicitly_wait(10)
if (driver.find_element_by_id("rememberMe").is_selected()):
    driver.find_element_by_id("rememberMe").click()
driver.find_element_by_name("submit").click()
driver.quit()