''' This module:
1. Login
2. Create a new project
3. Enables,imports and selects a folder for Box, DropBox, Figshare
** Code to delete the project is not added, as this module is used to enable,import and select folders for another module called 'DisconnectAllAcounts'
'''


# -*- coding: utf-8 -*-
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from Login import Login
from CreateProject import CreateProject


success = True



class EnableandImport:
    def is_alert_present(self, wd):
        try:
            wd.switch_to_alert().text
            return True
        except:
            return False
    def __init__(self, wd):
        try:
            l= Login(wd)
            c= CreateProject(wd)
            time.sleep(5)
            wd.find_element_by_xpath("//*[@id=\"projectSubnav\"]/div/div[2]/ul/li[8]/a").click() #("/html/body/div[4]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[3]/a[1]/div/div/div/div[1]/div/strong").click()
            time.sleep(3)
            
            #wd.find_element_by_xpath("/html/body/div[4]/div/div[1]/header/nav/div/div[2]/ul/li[8]/a").click()
            time.sleep(5)                           
            wd.find_element_by_css_selector("input[name=box]").click()
            time.sleep(5) 
            wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
            time.sleep(8) 
            
            wd.find_element_by_partial_link_text("Import").click()
        
            time.sleep(3)
            wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
            time.sleep(3)
            wd.find_element_by_css_selector("#tb-tbody > div > div > div:nth-child(6) > div.tb-td.tb-col-1.p-l-xs > input[type=\"radio\"]").click()
            time.sleep(3)
            wd.find_element_by_css_selector("#boxScope > div.box-settings > div > div > div.m-t-sm.addon-folderpicker-widget.box-widget > div.box-confirm-selection > form > div.pull-right > input").click()
            print("box is done")
            wd.find_element_by_css_selector("input[name=\"dropbox\"]").click()
            time.sleep(3) 
            wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
            time.sleep(5)
            wd.find_element_by_partial_link_text("Import").click()
            time.sleep(3)
            wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()  
            time.sleep(5)
            #wd.find_element_by_xpath("/html/body/div[4]/div/div[4]/div[2]/div[3]/div[2]/div[3]/div[1]/div/div/div[2]/div[1]/div/div/div/div[2]/div/div/div[5]/div[2]/input").click()
            #time.sleep(3)
            wd.find_element_by_css_selector("#tb-tbody > div > div > div:nth-child(2) > div.tb-td.tb-col-1.p-l-xs > input[type=\"radio\"]").click() ## selecting folder
            wd.find_element_by_css_selector("#dropboxScope .btn[value=Save]").click()
            time.sleep(3)
            print("dropbox done")
            wd.find_element_by_css_selector("input[name=\"figshare\"]").click()
            time.sleep(3) 
            wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
            time.sleep(3) 
            wd.find_element_by_css_selector("#figshareScope > h4.addon-title > small.authorized-by > span:nth-of-type(2) > a[href=\"#\"].text-primary.pull-right.addon-auth").click()
            time.sleep(3)
            wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
            time.sleep(30)  ##figshare folders take a lot of time to load
            wd.find_element_by_css_selector("#tb-tbody > div > div > div:nth-child(2) > div.tb-td.tb-col-1.p-l-xs > input[type=\"radio\"]").click()
            time.sleep(3)
            wd.find_element_by_css_selector("#figshareScope > div.figshare-settings > div > div > div.m-t-sm.addon-folderpicker-widget.figshare-widget > div.figshare-confirm-selection > form > div.pull-right > input").click()
            print("figshare done")
        finally:
            print("getting closer")
            if not success:
                raise Exception("Test failed.")
