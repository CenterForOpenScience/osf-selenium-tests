'''
Created on Jun 13, 2017
@author: shikhadubey
'''
import time
from selenium import webdriver

class Login:
   
    def __init__(self, driver):
    
        driver.get("https://staging.osf.io/")
        time.sleep(3)
        driver.find_element_by_partial_link_text("Sign In").click()
        time.sleep(3)
        driver.find_element_by_id("username").send_keys("shkd28892@gmail.com")
        time.sleep(3)
        driver.find_element_by_id('password').send_keys('Shikh@28892')
        time.sleep(3)
        driver.implicitly_wait(10)
        if (driver.find_element_by_id("rememberMe").is_selected()):
            driver.find_element_by_id("rememberMe").click()

        driver.find_element_by_name("submit").click()
