# -*- coding: utf-8 -*-
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
    wd.find_element_by_css_selector("input[name=box]").click()
    time.sleep(5) 
    wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
    time.sleep(5) 
    
    wd.find_element_by_css_selector("#boxScope > h4.addon-title > small.authorized-by > span:nth-of-type(2) > a[href=\"#\"].text-primary.pull-right.addon-auth").click()

    time.sleep(3)
    wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
    time.sleep(3)
   
    wd.find_element_by_xpath("/html/body/div[4]/div/div[4]/div[2]/div[3]/div[2]/div[1]/div[1]/div/div/div[2]/div[1]/div/div/div/div[2]/div/div/div[6]/div[2]/input").click()
    
    wd.find_element_by_css_selector("input[name=\"dropbox\"]").click()
    time.sleep(3) 
    wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
    time.sleep(3)
    wd.find_element_by_css_selector("#dropboxScope > h4.addon-title > small.authorized-by > span:nth-of-type(2) > a[href=\"#\"].text-primary.pull-right.addon-auth").click()
    time.sleep(3)
    wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
    time.sleep(8)
    wd.find_element_by_xpath("/html/body/div[4]/div/div[4]/div[2]/div[3]/div[2]/div[3]/div[1]/div/div/div[2]/div[1]/div/div/div/div[2]/div/div/div[5]/div[2]/input").click()
    time.sleep(3)
    wd.find_element_by_css_selector("#dropboxScope .btn[value=Save]").click()
    time.sleep(3)
    wd.find_element_by_css_selector("input[name=\"figshare\"]").click()
    time.sleep(3) 
    wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
    time.sleep(3) 
    wd.find_element_by_css_selector("#figshareScope > h4.addon-title > small.authorized-by > span:nth-of-type(2) > a[href=\"#\"].text-primary.pull-right.addon-auth").click()
    time.sleep(3)
    wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
    time.sleep(30)  ##figshare folders take a lot of time to load
    wd.find_element_by_xpath("/html/body/div[4]/div/div[4]/div[2]/div[3]/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div/div/div/div[2]/div/div/div[4]/div[2]/input").click()

finally:
    print("getting closer")
    if not success:
        raise Exception("Test failed.")
