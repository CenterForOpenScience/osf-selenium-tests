'''
This module: 
1. Login to staging
2. Creates a project from 'My Projects'
3. Creates a Component
4. Deletes the component
5. Deletes the project that has the component
Contains some refreshes due to nav bar issue (web page breaking), can be removed at leate stages
'''
from selenium import webdriver
import time
from Login import Login
from DeleteProject import DeleteProject

success= True
desired_cap = {'browser': 'Chrome', 'browser_version': '59.0', 'os': 'Windows', 'os_version': '10', 'resolution': '1024x768'}
wd= webdriver.Remote(
  command_executor='http://shikhadubey1:Mhtt1XkQq18k8nqQzsqn@hub.browserstack.com:80/wd/hub',
  desired_capabilities= desired_cap)
wd.implicitly_wait(60)

try:
    l= Login(wd)
    time.sleep(3)
    wd.refresh()
    wd.find_element_by_css_selector("#secondary-navigation > ul > li:nth-child(1) > a").click()
    time.sleep(3)
    wd.find_element_by_css_selector("#dashboard > div.dashboard-header > div > div.col-xs-4.p-sm > div > span > div.btn.btn-success.btn-success-high-contrast.f-w-xl").click()
    time.sleep(3)
    wd.find_element_by_name("projectName").send_keys("Testselenium")
    wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-success").click()
    time.sleep(3)
    wd.find_element_by_css_selector("#addProject > div > div > div > div.modal-footer > a").click()
    ###  Creating the component: code copied from CreateComponent 1
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