'''
Created on July 3, 2017

@author: patrickanderson
'''

from Login import Login
from CreateProject import CreateProject
from CreateFork import CreateFork

desired_cap = {'browser': 'Chrome', 'browser_version': '59.0', 'os': 'OS X', 'os_version': 'Sierra', 'resolution': '1920x1080'}

driver = webdriver.Remote(
    command_executor='http://patrickanderson2:Z39oMKMLFiyYJ88GWosk@hub.browserstack.com:80/wd/hub',
    desired_capabilities=desired_cap)

l = Login(driver)
time.sleep(3)
c = CreateProject(driver)
time.sleep(3)
f = CreateFork(driver)