from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from threading import Thread
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

class Contributors:
    def search_contributor(self, driver):
       
        driver.find_element_by_css_selector("#secondary-navigation > ul > li:nth-child(1) > a").click()
        time.sleep(3)
        driver.find_element_by_partial_link_text("Testselenium").click()
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id=\"projectSubnav\"]/div/div[2]/ul/li[7]/a").click()
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
        if not (len(driver.find_elements_by_css_selector("table.table-condensed")) != 0):
            raise Exception("assertElementPresent failed")
