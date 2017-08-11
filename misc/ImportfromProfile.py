'''
Created on Jun 16, 2017

@author: shikhadubey
'''
# -*- coding: utf-8 -*-
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from Login import Login
from time import time, sleep

class ImportfromProfile:

    def __init__(self, wd):   
        success = True
        try:
            l= Login(wd)
            sleep(5)
            wd.find_element_by_xpath("/html/body/div[4]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[2]/a[1]/div/div/div/div[1]/div/strong").click() #("/html/body/div[4]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[3]/a[1]/div/div/div/div[1]/div/strong").click()
            sleep(5)
            print("project clicked")
            wd.find_element_by_xpath("/html/body/div[4]/div/div[1]/header/nav/div/div[2]/ul/li[8]/a").click()
            sleep(3)
            wd.find_element_by_css_selector("#s3Scope > h4.addon-title > small.authorized-by > span:nth-of-type(2) > a[href=\"#\"].text-primary.pull-right.addon-auth").click()
            sleep(3)
            wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
            sleep(3)
            wd.find_element_by_css_selector("#boxScope > h4.addon-title > small.authorized-by > span:nth-of-type(2) > a[href=\"#\"].text-primary.pull-right.addon-auth").click()
            sleep(3)
            wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
            sleep(3)
            wd.find_element_by_css_selector("#dataverseScope > h4.addon-title > small.authorized-by > span:nth-of-type(2) > a[href=\"#\"].text-primary.pull-right.addon-auth").click()
            sleep(3)
            wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
            sleep(3)
            wd.find_element_by_css_selector("#dropboxScope > h4.addon-title > small.authorized-by > span:nth-of-type(2) > a[href=\"#\"].text-primary.pull-right.addon-auth").click()
            sleep(3)
            wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
            sleep(3)
            wd.find_element_by_css_selector("#configureAddons > .panel-body").click()
            sleep(3)
            wd.find_element_by_css_selector("#figshareScope > h4.addon-title > small.authorized-by > span:nth-of-type(2) > a[href=\"#\"].text-primary.pull-right.addon-auth").click()
            sleep(3)
            wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
            sleep(3)
            wd.find_element_by_css_selector("#githubImportToken").click()
            sleep(3)
            wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
            sleep(3)
            wd.find_element_by_css_selector("a[href=\"#\"].text-primary").click()
            sleep(3)
            wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
            sleep(3)
            wd.find_element_by_xpath("/html/body/div[4]/div/div[4]/div[2]/div[3]/div[2]/div[5]/h4/small/span[2]/a").click()
            time.sleep(3)
            wd.find_element_by_xpath("/html/body/div[6]/div/div/div[3]/button[2]").click()
            time.sleep(3)
            wd.find_element_by_xpath("/html/body/div[4]/div/div[4]/div[2]/div[3]/div[2]/div[5]/div[1]/div/div/div[2]/div[1]/div/div/div/div[2]/div/div/div[2]/div[2]/input").click()
            
        
        finally:
            print('Done')
            if not success:
                raise Exception("Test failed.")
