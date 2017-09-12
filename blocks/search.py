from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from threading import Thread
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time


class Search:

    def staging_navbar(self, driver):
        driver.get("https://staging.osf.io/")
        time.sleep(3)
        driver.find_element_by_css_selector("#primary-navigation > span").click()
        time.sleep(2)
        driver.find_element_by_css_selector("#navbarScope > div > div.navbar-header > div.dropdown.primary-nav.open > ul > li:nth-child(1) > a > b").click()
        #assert driver.current_url = "https://staging.osf.io/"
        time.sleep(3)
        driver.back()
        time.sleep(3)
        driver.find_element_by_css_selector("#primary-navigation > span").click()
        time.sleep(2)
        driver.find_element_by_css_selector("#navbarScope > div > div.navbar-header > div.dropdown.primary-nav.open > ul > li:nth-child(2) > a > b").click()
        
        
