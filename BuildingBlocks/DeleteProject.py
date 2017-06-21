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


class DeleteProject:
    
    def __init__(self, driver):
        time.sleep(8)
        driver.find_element_by_partial_link_text("test").click()

        driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/header/nav/div/div[2]/ul/li[8]/a").click()  #//project settings
           
        driver.find_element_by_xpath("/html/body/div[4]/div/div[4]/div[2]/div[1]/div[2]/button[3]").click() # // Click delete
        time.sleep(8)
        inputelement= driver.find_element_by_xpath("/html/body/div[6]/div/div/div[2]/div/p[2]")
        OSNAMES = inputelement.text
    
        a,b,c,d,e, f= OSNAMES.split()
        print f
    
        driver.find_element_by_id("bbConfirmText").send_keys(f)
        time.sleep(8)
        driver.find_element_by_xpath("/html/body/div[6]/div/div/div[3]/button[2]").click()
        time.sleep(8)
       
    
    
    
    