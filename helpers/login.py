'''
Created on Aug 10, 2017

@author: shikhadubey
'''
import settings

def login(driver):
    driver.get("https://staging.osf.io/")
    driver.find_element_by_partial_link_text("Sign In").click()
    driver.find_element_by_id("username").send_keys(settings.USER_ONE)
    driver.find_element_by_id('password').send_keys(settings.USER_ONE_PASSWORD)
    if (driver.find_element_by_id("rememberMe").is_selected()):
        driver.find_element_by_id("rememberMe").click()
    driver.find_element_by_name("submit").click()
