'''
Created on Aug 22, 2017

@author: patrickanderson
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from threading import Thread
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time


class CreateNodes:

    def create_project(self, driver):
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id='osfHome']/div[3]/div/div/div/div/div/m-b-lg/div/span/button").click()
        time.sleep(3)
        driver.find_element_by_name("projectName").send_keys("Testselenium")
        driver.find_element_by_xpath("//*[@id='addProjectFromHome']/div/div/div[3]/button[2]").click()
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id='addProjectFromHome']/div/div/div/div[2]/a").click()