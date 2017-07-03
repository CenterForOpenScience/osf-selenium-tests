'''
Created on July 3, 2017

@author: patrickanderson
'''

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from Login import Login
from CreateProject import CreateProject
from CreateFork import CreateFork
import time

desired_cap = {'browser': 'Chrome', 'browser_version': '59.0', 'os': 'OS X', 'os_version': 'Sierra', 'resolution': '1920x1080'}

driver = webdriver.Remote(
    command_executor='http://patrickanderson2:Z39oMKMLFiyYJ88GWosk@hub.browserstack.com:80/wd/hub',
    desired_capabilities=desired_cap)

l = Login(driver)
time.sleep(3)
driver.get("https://osf.io/t5p76/")
time.sleep(3)
f = CreateFork(driver)
driver.quit()