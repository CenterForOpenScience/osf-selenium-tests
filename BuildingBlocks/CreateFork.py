'''
Created on July 3, 2017

@author: patrickanderson
'''
from selenium.webdriver.support import expected_conditions as EC
import time
import unittest

class CreateFork(unittest.TestCase):

    def __init__(self, driver):
    	
        time.sleep(3)
        driver.find_element_by_xpath("//a[text()='Forks']").click()
        time.sleep(3)
        driver.find_element_by_xpath("//a[text()='New fork']").click()
        time.sleep(3)
        driver.find_element_by_xpath("//button[text()='Fork']").click()
        time.sleep(5)
        driver.find_element_by_xpath("//button[text()='Go to new fork']").click()
        time.sleep(3)
        assert "Fork of Testselenium" in driver.find_element_by_id("nodeTitleEditable")
        # self.assertTrue(EC.text_to_be_present_in_element(driver.find_element_by_id("nodeTitleEditable"), "1")) #We will likely change this