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
from selenium.webdriver import firefox
from Login import Login
from CreateProject import CreateProject

class AddReadOnlyUser(object):
    driver = webdriver.Firefox()
    #def __init__(self, driver):
    l= Login(driver)
    c= CreateProject(driver)
    time.sleep(3)
    driver.find_element_by_partial_link_text("Contributors").click()
    time.sleep(3)
    driver.find_element_by_xpath("/html/body/div[4]/div/div[8]/div[1]/h3/a").click()
    time.sleep(3)
    driver.find_element_by_xpath("/html/body/div[4]/div/div[4]/div/div/div[2]/div[1]/form/div/div/div[1]/input").send_keys("QA Ghost 2")
    time.sleep(3)
    driver.find_element_by_xpath("/html/body/div[4]/div/div[4]/div/div/div[2]/div[1]/form/div/div/div[1]/span/input").click()
    time.sleep(6)
    driver.find_element_by_xpath("/html/body/div[4]/div/div[4]/div/div/div[2]/div[1]/div/div[1]/table/tbody/tr[1]/td[1]/a/i").click()
    
    #xpath("/html/body/div[4]/div/div[4]/div/div/div[2]/div[1]/form/div/div/div[1]/span/input").click()
    print("found and clicked + sign")
    time.sleep(6)
    driver.find_element_by_xpath("/html/body/div[4]/div/div[4]/div/div/div[2]/div[1]/div/div[2]/table/tbody/tr/td[4]/select").click()
    time.sleep(3)
    driver.find_element_by_xpath("/html/body/div[4]/div/div[4]/div/div/div[2]/div[1]/div/div[2]/table/tbody/tr/td[4]/select/option[1]").click()
    driver.find_element_by_xpath("/html/body/div[4]/div/div[4]/div/div/div[3]/span[2]/a[1]").click()
    driver.find_element_by_xpath("/html/body/div[4]/div/div[4]/div/div/div[2]/div[1]/div/div[2]/table/tbody/tr/td[4]/select").click() #Click on the menu 
    time.sleep(3)
    print("Contributor added successfully")
