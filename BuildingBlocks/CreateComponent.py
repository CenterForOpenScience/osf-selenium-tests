'''
This module:
1. Login to staging
2. Create a new projrct fromdashboard
3. Create new component
4. Go to the created component--> delete the component
5. Delete the parent project
ps: The script contains some  refreshes (due to the webpage breaking, feel free to remove them )
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from Login import Login
from CreateProject import CreateProject
from DeleteProject import DeleteProject

success= True
desired_cap = {'browser': 'Chrome', 'browser_version': '59.0', 'os': 'Windows', 'os_version': '10', 'resolution': '1024x768'}
wd= webdriver.Remote(
  command_executor='http://shikhadubey1:Mhtt1XkQq18k8nqQzsqn@hub.browserstack.com:80/wd/hub',
  desired_capabilities= desired_cap)
wd.implicitly_wait(60)

#class CommentCreate:
    #def __init__(self, driver):
try:
    l= Login(wd)
    time.sleep(3)
    wd.refresh()
    time.sleep(5)
    c= CreateProject(wd)
    
    wd.refresh()
    time.sleep(5)
    wd.refresh()
    wd.refresh()
    time.sleep(3)
    wd.find_element_by_css_selector("#newComponent > span > div.btn.btn-sm.btn-default").click()
    time.sleep(3)
    wd.find_element_by_name("projectName").send_keys("This is a component")
    wd.find_element_by_css_selector("input[name=\"inherit_contributors\"]").click()
    time.sleep(3)
    wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-success").click()
    wd.find_element_by_css_selector("#addSubComponent > div > div > div > div.modal-footer > a").click()
    print("Component created and now you are inside that component")
    print("Proceeding with the delete")
    wd.refresh()
    wd.find_element_by_css_selector("#projectSubnav > div > div.collapse.navbar-collapse.project-nav > ul > li:nth-child(9) > a").click()
    print("Settings clicked")
    wd.find_element_by_id("deleteNode").click()
    time.sleep(8)
    
    inputelement= wd.find_element_by_xpath("/html/body/div[6]/div/div/div[2]/div/p[2]")
    OSNAMES = inputelement.text

    a,b,c,d,e, f= OSNAMES.split()
    print ("The text to be input is:",f)
    wd.find_element_by_id("bbConfirmText").send_keys(f)
    time.sleep(8)
    wd.find_element_by_xpath("/html/body/div[6]/div/div/div[3]/button[2]").click()
    time.sleep(8)
    print("Component successfully deleted, now proceeding with deletion of project")
    p= DeleteProject(wd)
    print("The project is also deleted, Yayyy!!!")
finally:
    wd.quit()