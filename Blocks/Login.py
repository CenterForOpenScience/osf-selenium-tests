'''
Created on Jul 21, 2017

@author: patrickanderson
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from threading import Thread
import time#
from selenium.webdriver.support.select import Select
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class Login:
   
    def staging_login(self, driver):
        driver.get("https://staging.osf.io/")
        time.sleep(3)
        driver.find_element_by_partial_link_text("Sign In").click()
        time.sleep(3)
        driver.find_element_by_id("username").send_keys("osframeworktesting+ghost@gmail.com")
        time.sleep(3)
        driver.find_element_by_id('password').send_keys('\"Repr0duce!\"')
        time.sleep(3)
        driver.implicitly_wait(10)
        if (driver.find_element_by_id("rememberMe").is_selected()):
            driver.find_element_by_id("rememberMe").click()
            
        driver.find_element_by_name("submit").click()

    def production_login(self, driver):
        driver.get("https://osf.io/")
        time.sleep(3)
        driver.find_element_by_partial_link_text("Sign In").click()
        time.sleep(3)
        driver.find_element_by_id("username").send_keys("osframeworktesting+ghost@gmail.com")
        time.sleep(3)
        driver.find_element_by_id('password').send_keys('\"Repr0duce!\"')
        time.sleep(3)
        driver.implicitly_wait(10)
        if (driver.find_element_by_id("rememberMe").is_selected()):
            driver.find_element_by_id("rememberMe").click()
            
        driver.find_element_by_name("submit").click()