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
        assert "https://staging.osf.io/" in driver.current_url
        time.sleep(3)
        driver.find_element_by_css_selector("#primary-navigation > span").click()
        time.sleep(1)
        driver.find_element_by_css_selector("#navbarScope > div > div.navbar-header > div.dropdown.primary-nav.open > ul > li:nth-child(2) > a > b").click()
        assert "https://staging.osf.io/preprints/" in driver.current_url
        time.sleep(2)
        driver.back() 
        time.sleep(3)
        driver.find_element_by_css_selector("#primary-navigation > span").click()
        driver.find_element_by_css_selector("#navbarScope > div > div.navbar-header > div.dropdown.primary-nav.open > ul > li:nth-child(3) > a > b").click()
        assert "https://staging.osf.io/registries/" in driver.current_url
        time.sleep(2)
        driver.back()
        time.sleep(2)
        driver.find_element_by_css_selector("#primary-navigation > span").click()
        driver.find_element_by_css_selector("#navbarScope > div > div.navbar-header > div.dropdown.primary-nav.open > ul > li:nth-child(4) > a > b").click()
        assert "https://staging.osf.io/meetings" in driver.current_url
        time.sleep(2)
        driver.back()
        driver.find_element_by_css_selector("#secondary-navigation > ul > li:nth-child(2) > a").click()
        assert "https://staging.osf.io/support/" in driver.current_url
        driver.back()
        time.sleep(2)
        driver.find_element_by_css_selector("#secondary-navigation > ul > li.navbar-donate-button > a").click()
        assert "https://cos.io/donate-to-cos/" in driver.current_url
        time.sleep(2)
        driver.back()
        
    def staging_search_navbar(self, driver):        
        driver.find_element_by_css_selector("#secondary-navigation > ul > li:nth-child(1) > a").click() #Search

        assert "https://staging.osf.io/search/" in driver.current_url
        driver.find_element_by_css_selector("#searchControls > div.osf-search > div > div > div > form > span > button:nth-child(2) > i").click()
        time.sleep(3)
        input_element = driver.find_element_by_css_selector("#search-help-modal > div > div > div.modal-header > h3")
        modal1 = input_element.text
        assert modal1 == "Search help"
        driver.find_element_by_css_selector("#search-help-modal > div > div > div.modal-body > p > a").click()
        time.sleep(2)
        assert "http://extensions.xwiki.org/xwiki/bin/view/Extension/Search+Application+Query+Syntax" in driver.current_url
        #driver.back()
        time.sleep(2)
        #driver.find_element_by_css_selector("#search-help-modal > div > div > div.modal-footer > button").click()
        driver.back()
        time.sleep(2)
        driver.find_element_by_css_selector("#searchPageFullBar").send_keys("*", Keys.RETURN)
        time.sleep(2)
        driver.find_element_by_css_selector("#searchPageFullBar").clear()
        driver.find_element_by_css_selector("#searchPageFullBar").send_keys("staging.osf.io/52vej/", Keys.RETURN)
        time.sleep(2)
