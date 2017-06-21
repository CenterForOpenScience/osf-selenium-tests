'''
Created on Jun 14, 2017

@author: shikhadubey
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

class Logout:
    
    def __init__(self, driver):
        driver.find_element_by_xpath("/html/body/div[2]/nav/div/div[2]/ul/li[5]/a").click()
        time.sleep(5)
        driver.find_element_by_partial_link_text("Log out").click()
        
        