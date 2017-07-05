'''
This module:
1. Logs in to staging
2. Creates a project from "My Project" page
'''
import time#
from Login import Login
from selenium import webdriver

desired_cap = {'browser': 'Chrome', 'browser_version': '59.0', 'os': 'Windows', 'os_version': '10', 'resolution': '1024x768'}
wd= webdriver.Remote(
  command_executor='http://shikhadubey1:Mhtt1XkQq18k8nqQzsqn@hub.browserstack.com:80/wd/hub',
  desired_capabilities= desired_cap)
wd.implicitly_wait(60)

try:    
    l= Login(wd)
    time.sleep(3)
    wd.refresh()
    wd.find_element_by_xpath("//*[@id=\"secondary-navigation\"]/ul/li[1]/a").click()
    time.sleep(3)
    wd.find_element_by_css_selector("#dashboard > div.dashboard-header > div > div.col-xs-4.p-sm > div > span > div.btn.btn-success.btn-success-high-contrast.f-w-xl").click()
    wd.find_element_by_name("projectName").send_keys("Testselenium")
    wd.find_element_by_css_selector("#addProject > div > div > div.modal-footer > button.btn.btn-success").click()
    print("Project Created")
    wd.find_element_by_css_selector("#addProject > div > div > div > div.modal-footer > a").click()
    print("You are inside your brand new project")
    time.sleep(3)

    
finally:
    wd.quit