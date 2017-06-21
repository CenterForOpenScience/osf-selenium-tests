'''
Created on Jun 19, 2017

@author: shikhadubey
'''
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from Login import Login


success = True
wd = WebDriver()
wd.implicitly_wait(60)

def is_alert_present(wd):
    try:
        wd.switch_to_alert().text
        return True
    except:
        return False

try:
    l= Login(wd)
    time.sleep(5)
    wd.find_element_by_xpath("/html/body/div[4]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[2]/a[1]/div/div/div/div[1]/div/strong").click() #("/html/body/div[4]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[3]/a[1]/div/div/div/div[1]/div/strong").click()
    time.sleep(3)
    print("project clicked")
    time.sleep(3)
    wd.find_element_by_xpath("/html/body/div[4]/div/div[1]/header/nav/div/div[2]/ul/li[8]/a").click()
    time.sleep(5)                           
    wd.find_element_by_css_selector("input[name=\"github\"]").click()
    time.sleep(3) 
    wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
    time.sleep(3) 
    wd.find_element_by_css_selector("#githubImportToken").click()
    time.sleep(3)
    wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
    time.sleep(3)
    wd.find_element_by_xpath("/html/body/div[4]/div/div[4]/div[2]/div[3]/div[2]/form/div[2]/div[1]/select").click()
    time.sleep(3)
    wd.find_element_by_xpath("/html/body/div[4]/div/div[4]/div[2]/div[3]/div[2]/form/div[2]/div[1]/select/option[2]").click()
    time.sleep(3)
    wd.find_element_by_xpath("/html/body/div[4]/div/div[4]/div[2]/div[3]/div[2]/form/div[2]/div[2]/button").click()
    wd.find_element_by_css_selector("input[name=\"googledrive\"]").click()
    time.sleep(3) 
    wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
    time.sleep(5) 
    wd.find_element_by_css_selector("#googledriveScope > h4.addon-title > small.authorized-by > span:nth-of-type(2) > a[href=\"#\"].text-primary.pull-right.addon-auth").click()#("/html/body/div[4]/div/div[4]/div[2]/div[3]/div[2]/div[5]/h4/small/span[2]/a").click()
    time.sleep(3)
    wd.find_element_by_xpath("/html/body/div[6]/div/div/div[3]/button[2]").click()
    time.sleep(3)
    wd.find_element_by_xpath("/html/body/div[4]/div/div[5]/div[2]/div[3]/div[2]/div[5]/div[1]/div/div/div[2]/div[1]/div/div/div/div[2]/div/div/div[6]/div[2]/input").click()
    time.sleep(3)
    wd.find_element_by_xpath("/html/body/div[4]/div/div[5]/div[2]/div[3]/div[2]/div[5]/div[1]/div/div/div[2]/div[2]/form/div[2]/input").click()
    time.sleep(3)
    wd.find_element_by_xpath("/html/body/div[4]/div/div[5]/div[2]/div[2]/div[2]/form/div[9]/label/input").click()
    time.sleep(3)
    wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
    time.sleep(3)
    wd.find_element_by_xpath("/html/body/div[4]/div/div[5]/div[2]/div[3]/div[2]/div[6]/h4/small/span[2]/a").click()
    time.sleep(3)
    wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
    time.sleep(3)
    wd.find_element_by_xpath("/html/body/div[4]/div/div[5]/div[2]/div[3]/div[2]/div[6]/div[2]/div/div/div[2]/div[1]/div/div/div/div[2]/div/div/div[2]/div[2]/input").click()
    time.sleep(3)
    wd.find_element_by_xpath("/html/body/div[4]/div/div[5]/div[2]/div[3]/div[2]/div[6]/div[2]/div/div/div[2]/div[2]/form/div[2]/input").click()
    wd.find_element_by_css_selector("input[name=\"s3\"]").click()
    time.sleep(3) 
    wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
    time.sleep(3) 
    wd.find_element_by_css_selector("#s3Scope > h4.addon-title > small.authorized-by > span:nth-of-type(2) > a[href=\"#\"].text-primary.pull-right.addon-auth").click()#("/html/body/div[4]/div/div[4]/div[2]/div[3]/div[2]/div[5]/h4/small/span[2]/a").click()
    time.sleep(3)
    wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
    time.sleep(3)
    wd.find_element_by_xpath("/html/body/div[4]/div/div[4]/div[2]/div[3]/div[2]/div[1]/div[2]/div/div/div[2]/div[1]/div/div/div/div[2]/div/div/div[6]/div[2]/input").click()
    time.sleep(3)
    wd.find_element_by_xpath("/html/body/div[4]/div/div[4]/div[2]/div[3]/div[2]/div[1]/div[2]/div/div/div[2]/div[2]/form/div[2]/input").click()
finally:
    print("getting closer")
    if not success:
        raise Exception("Test failed.")
