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
import settings
from selenium import webdriver

#CE = os.environ['CE']
#DESIRED_CAP= os.environ['DESIRED_CAP']
#DC = {'browser': 'Chrome', 'browser_version': '61.0', 'os': 'Windows', 'os_version': '10', 'resolution': '2048x1536'}
#DRIVER=webdriver.Remote({CE},desired_capabilities=DC)

def osf_meetings_landing_page(driver):
    driver.get("https://staging.osf.io/meetings/")
    time.sleep(3)
    driver.find_element_by_css_selector("#primary-navigation > span").click()
    time.sleep(2)
    driver.find_element_by_css_selector("#navbarScope > div > div.navbar-header > div.dropdown.primary-nav.open > ul > li:nth-child(1) > a > b").click()
    assert "https://staging.osf.io/" in driver.current_url
    time.sleep(3)
    driver.back()
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
    driver.find_element_by_css_selector("#primary-navigation > span").click()
    driver.find_element_by_css_selector("#navbarScope > div > div.navbar-header > div.dropdown.primary-nav.open > ul > li:nth-child(4) > a > b").click()
    assert "https://staging.osf.io/meetings" in driver.current_url
    time.sleep(2)

    driver.find_element_by_css_selector("#secondary-navigation > ul > li:nth-child(2) > a").click()
    #assert "https://staging.osf.io/support/" in driver.current_url
    driver.back()
    time.sleep(2)
    driver.find_element_by_css_selector("#secondary-navigation > ul > li.navbar-donate-button > a").click()
    assert "https://cos.io/donate-to-cos/" in driver.current_url
    time.sleep(2)
    driver.back()

def osf_meetings_sign_in(driver):

    driver.find_element_by_partial_link_text("Sign In").click()
    driver.find_element_by_id("username").send_keys(settings.USERNAME_ONE)
    driver.find_element_by_id('password').send_keys(settings.PASSWORD)
    if (driver.find_element_by_id("rememberMe").is_selected()):
        driver.find_element_by_id("rememberMe").click()
    driver.find_element_by_name("submit").click()
    driver.find_element_by_css_selector("body > div.watermarked > div.osf-meeting-header-img > div > div > div.row > div:nth-child(1) > div.p-v-md > button").click()
    time.sleep(2)
    assert "https://staging.osf.io/meetings" in driver.current_url
    element = driver.find_element_by_css_selector("#osf-meeting-register > div > p:nth-child(1)")
    assert element.text == "OSF for Meetings is a product that we offer to academic conferences at no cost. To request poster and talk hosting for a conference:"
    driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/div[3]/div[2]/div[2]/button").click()
    e1 = driver.find_element_by_css_selector("#osf-meeting-upload > div > p:nth-child(1)")
    assert e1.text == "The OSF can host posters and talks for scholarly meetings. Submitting a presentation is easy:"
    e2 = driver.find_element_by_css_selector("#osf-meeting-upload > div > ul > li:nth-child(1)")
    assert e2.text == "Find the email address for your conference by clicking on its name in the list below"
    e3 = driver.find_element_by_css_selector("#osf-meeting-upload > div > ul > li:nth-child(2)")
    assert e3.text == "Send your materials to the OSF for Meetings email address for your conference"
    #e4 = driver.find_element_by_css_selector("#osf-meeting-upload > div > p:nth-child(3)")


def osf_meetings_search_meeting(driver):
    #Selenium not sending numeric '2015' in send_keys...
    search_text="OSF for"
    driver.find_element_by_css_selector("#meetings-grid > div > div > div.tb-head > div > input").send_keys(search_text, Keys.ENTER)
    assert driver.find_element_by_link_text("OSF for Meetings 2015").is_displayed()

def osf_meeting_bottom_bar(driver):
    driver.get("https://staging.osf.io/meetings/")
    driver.find_element_by_css_selector("body > div.container.copyright > div > div > p > a:nth-child(1)").click()
    assert "https://cos.io/" in driver.current_url
    time.sleep(2)
    driver.back()
    driver.find_element_by_partial_link_text("Terms of Use").click()
    assert "https://github.com/CenterForOpenScience/cos.io/blob/master/TERMS_OF_USE.md" in driver.current_url
    time.sleep(3)
    driver.back()
    driver.find_element_by_css_selector("body > div.container.copyright > div > div > p > a:nth-child(3)").click()
    assert "https://github.com/CenterForOpenScience/cos.io/blob/master/PRIVACY_POLICY.md" in driver.current_url
    driver.back()
