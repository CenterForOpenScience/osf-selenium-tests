from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from threading import Thread
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.common.action_chains import ActionChains
import os

#command_executor = os.environ['command_executor']
#DRIVER= webdriver.Remote(command_executor, desired_capabilities=DESIRED_CAP)
#print(shikha)
CE = os.environ['CE']
#DESIRED_CAP= os.environ['DESIRED_CAP']
DC = {'browser': 'Chrome', 'browser_version': '61.0', 'os': 'Windows', 'os_version': '10', 'resolution': '2048x1536'}
DRIVER=webdriver.Remote({CE},desired_capabilities=DC)
def search_add_contributor(driver):
   
    driver.find_element_by_css_selector("#secondary-navigation > ul > li:nth-child(1) > a").click()
    time.sleep(3)
    driver.find_element_by_partial_link_text("Testselenium").click()
    time.sleep(3)
    driver.find_element_by_css_selector("#projectSubnav > div > div.collapse.navbar-collapse.project-nav > ul > li:nth-child(7) > a").click()
    time.sleep(3)
    driver.find_element_by_css_selector("#manageContributors > h3 > a").click()
    time.sleep(3)
    driver.find_element_by_css_selector("input[placeholder=\"Search by name\"]").click()
    time.sleep(3)
    driver.find_element_by_css_selector("input[placeholder=\"Search by name\"]").clear()
    time.sleep(3)
    driver.find_element_by_css_selector("input[placeholder=\"Search by name\"]").send_keys("QA Ghost 2")
    time.sleep(3)
    driver.find_element_by_css_selector("input[type=\"submit\"]").click()
    #driver.find_element_by_css_selector("#addContributors > div > div > div.modal-body > div:nth-child(1) > div > div:nth-child(1) > table > tbody > tr:nth-child(1) > td.p-r-sm.osf-icon-td > a > i").click()
    time.sleep(2)
    if not (len(driver.find_elements_by_css_selector("table.table-condensed")) != 0):
        raise Exception("assertElementPresent failed")
    time.sleep(2)
    driver.find_element_by_css_selector("#addContributors > div > div > div.modal-body > div:nth-child(1) > div > div:nth-child(1) > table > tbody > tr:nth-child(1) > td.p-r-sm.osf-icon-td > a > i").click()
    driver.find_element_by_css_selector("#addContributors > div > div > div.modal-footer > span:nth-child(3) > a.btn.btn-success").click()
    time.sleep(3)
    
def changetoread_contributor(driver):
   
    driver.find_element_by_css_selector("#contributors > tr:nth-child(2) > td.permissions > div.td-content > span:nth-child(1) > select").click()
    element= driver.find_element_by_css_selector("#contributors > tr:nth-child(2) > td.permissions > div.td-content > span:nth-child(1) > select").send_keys("read", Keys.ENTER)
    #element.send_keys(Keys.ENTER)
    time.sleep(3)
    driver.find_element_by_css_selector("#manageContributors > div.m-b-sm > a.btn.btn-success.contrib-button").click()
    driver.find_element_by_css_selector("button[type=\"button\"].btn.btn-success").click()
    time.sleep(3)

def reorder_contributor(driver):
    time.sleep(3)
    source_element = driver.find_element_by_xpath('//*[@id="contributors"]/tr[2]/td[2]/span[2]/a')
    dest_element = driver.find_element_by_xpath('//*[@id="contributors"]/tr[1]/td[2]/span[2]/a')
    ActionChains(driver).drag_and_drop(source_element, dest_element).perform()
    time.sleep(3)
    driver.find_element_by_css_selector("#manageContributors > div.m-b-sm > a.btn.btn-success.contrib-button").click()
    time.sleep(2)
    driver.find_element_by_css_selector("button[type=\"button\"].btn.btn-success").click()
    time.sleep(3)
