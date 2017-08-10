'''
Created on Aug 8, 2017

@author: patrickanderson
'''
import pytest


class BuildingBlocks:

    def test_login(self, driver):
        
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