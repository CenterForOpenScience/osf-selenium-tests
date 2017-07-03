'''
Created on Jun 16, 2017

@author: shikhadubey
'''

# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from threading import Thread
from selenium.webdriver.support.select import Select
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import firefox
from Login import Login 
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

#class AddonEnable:
wd= webdriver.Firefox()
    #def __init__(self, wd):
success = True
try:
   
    l= Login(wd)
    time.sleep(5)
    wd.find_element_by_css_selector("html body div#osfHome div.quickSearch div.container.p-t-lg div.row.m-t-lg div.col-md-10.col-md-offset-1.col-lg-8.col-lg-offset-2 div.row div.col-xs-12 div.row.quick-project div.col-xs-12 div.quick-search-table div a div.m-v-sm.node-styling div.row div div.col-sm-3.col-md-6.p-v-xs div.quick-search-col strong").click()#partial_link_text("Test").click()#)css_selector(".quick-search-table > div:nth-child(2) > a:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(1)").click()#xpath("/html/body/div[4]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[2]/a[1]/div/div/div/div[1]/div/strong").click() #("/html/body/div[4]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[3]/a[1]/div/div/div/div[1]/div/strong").click()
    time.sleep(3)
    print("project clicked")
    time.sleep(3)
    wd.find_element_by_xpath("/html/body/div[4]/div/div[1]/header/nav/div/div[2]/ul/li[8]/a").click()
    time.sleep(3)                                         
    
    wd.find_element_by_css_selector("input[name=\"s3\"]").click()
    time.sleep(3) 
    wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
    time.sleep(3) 
    wd.find_element_by_css_selector("input[name=\"box\"]").click()
    time.sleep(3) 
    wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
    time.sleep(3) 
    wd.find_element_by_css_selector("input[name=\"dataverse\"]").click()
    time.sleep(3) 
    wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
    time.sleep(3) 
    wd.find_element_by_css_selector("input[name=\"dropbox\"]").click()
    time.sleep(3) 
    wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
    time.sleep(3) 
    wd.find_element_by_css_selector("input[name=\"figshare\"]").click()
    time.sleep(3) 
    wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
    time.sleep(3) 
    wd.find_element_by_css_selector("input[name=\"github\"]").click()
    time.sleep(3) 
    wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
    time.sleep(3) 
    wd.find_element_by_css_selector("input[name=\"googledrive\"]").click()
    time.sleep(3) 
    wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
    time.sleep(3) 
finally:
    print("in progress")
    if not success:
        raise Exception("Test failed.")
