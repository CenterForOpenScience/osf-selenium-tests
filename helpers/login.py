'''
Created on Aug 10, 2017

@author: shikhadubey
'''
import settings
from selenium import webdriver

def login(driver):
    driver.get(settings.DOMAIN)
    driver.find_element_by_partial_link_text("Sign In").click()
    driver.find_element_by_id("username").send_keys(settings.USERNAME_ONE)
    if (settings.DOMAIN == "http://localhost:5000/"):
        driver.find_element_by_id("submit").click()
    else:
        driver.find_element_by_id('password').send_keys(settings.PASSWORD)
        if (driver.find_element_by_id("rememberMe").is_selected()):
            driver.find_element_by_id("rememberMe").click()
        driver.find_element_by_name("submit").click()

    # driver.implicitly_wait(10) # The pages takes a few seconds to load
