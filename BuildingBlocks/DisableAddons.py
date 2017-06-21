'''
Created on Jun 16, 2017

@author: shikhadubey
'''
# -*- coding: utf-8 -*-
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from Login import Login
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

class DisableAddons:
   
    def __init__(self, wd):
        success= True

        try:
            l= Login(wd)
            time.sleep(8)
            wd.find_element_by_xpath("/html/body/div[4]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[2]/a[1]/div/div/div/div[1]/div/strong").click() #("/html/body/div[4]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[3]/a[1]/div/div/div/div[1]/div/strong").click()
            time.sleep(3)
            print("project clicked")
            time.sleep(3)
            wd.find_element_by_xpath("/html/body/div[4]/div/div[1]/header/nav/div/div[2]/ul/li[8]/a").click()
            time.sleep(3) 
            wd.find_element_by_css_selector("input[name=\"googledrive\"]").click()
            time.sleep(3)
            wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-danger").click()
            time.sleep(3)
            
            wd.find_element_by_css_selector("input[name=\"github\"]").click()
            time.sleep(3)
            wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-danger").click()
            time.sleep(3)
            print("github done")
            time.sleep(3)
            wd.find_element_by_css_selector("input[name=\"box\"]").click()
            time.sleep(3) 
            wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-danger").click()
            time.sleep(3)
            wd.find_element_by_css_selector("input[name=\"figshare\"]").click()
            time.sleep(3) 
            wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-danger").click()
            time.sleep(3)
            wd.find_element_by_css_selector("input[name=\"dropbox\"]").click()
            time.sleep(3) 
            wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-danger").click()
            time.sleep(3) 
            wd.find_element_by_css_selector("input[name=\"dataverse\"]").click()
            time.sleep(3) 
            wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-danger").click()
            time.sleep(3) 
            
            wd.find_element_by_css_selector("input[name=\"s3\"]").click()
         
            time.sleep(3) 
            wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-danger").click()
            wd.find_element_by_xpath("/html/body/div[4]/div/div[1]/header/nav/div/div[2]/ul/li[8]/a").click()
          
            time.sleep(3)
        finally:
            print("done")
            if not success:
                raise Exception("Test failed.")
    

