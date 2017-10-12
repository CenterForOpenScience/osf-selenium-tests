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

def osf_bottom_bar(driver):
  #Explore
  driver.find_element_by_xpath("/html/body/footer/div/div/div[1]/ul/li[1]/a").click()
  assert "https://staging.osf.io/activity/" in driver.current_url
  driver.back()
  #driver.find_element_by_xpath("/html/body/footer/div/div/div[1]/ul/li[2]/a").click()
   #assert "https://staging.osf.io/activity/" in driver.current_url
  #FAQ/Guidlines
  driver.find_element_by_xpath("/html/body/footer/div/div/div[1]/ul/li[3]/a").click()
  assert "https://staging.osf.io/support/" in driver.current_url
  driver.back()
  #API
  driver.find_element_by_xpath("/html/body/footer/div/div/div[1]/ul/li[4]/a").click()
  assert "https://api.osf.io/v2/" in driver.current_url
  driver.back()
  #SourceCode
  driver.find_element_by_xpath("/html/body/footer/div/div/div[1]/ul/li[5]/a").click()
  assert "https://github.com/CenterForOpenScience/osf.io" in driver.current_url
  driver.back()
  #Home
  driver.find_element_by_xpath("/html/body/footer/div/div/div[2]/ul/li[1]/a").click()
  assert "https://cos.io/" in driver.current_url
  driver.back()
  #driver.find_element_by_xpath("/html/body/footer/div/div/div[2]/ul/li[2]/a").click()
  
  #guidlines
  driver.find_element_by_xpath("/html/body/footer/div/div/div[2]/ul/li[4]/a").click()
  assert "https://cos.io/our-services/top-guidelines/" in driver.current_url
  driver.back()
  #Donate
  driver.find_element_by_xpath("/html/body/footer/div/div/div[2]/ul/li[5]/a").click()
  assert "https://www.crowdrise.com/donate/charity/centerforopenscience" in driver.current_url
  driver.back()
  Twitter
  driver.find_element_by_xpath("/html/body/footer/div/div/div[3]/a[1]/i").click()
  assert "https://twitter.com/OSFramework" in driver.current_url
  driver.back()
  #Facebook
  driver.find_element_by_xpath("/html/body/footer/div/div/div[3]/a[2]/i").click()
  assert "https://www.facebook.com/CenterForOpenScience/" in driver.current_url
  driver.back()
  #Google forum
  driver.find_element_by_xpath("/html/body/footer/div/div/div[3]/a[3]/i").click()
  assert "https://groups.google.com/forum/#!forum/openscienceframework" in driver.current_url
  driver.back()
#Github
  driver.find_element_by_xpath("/html/body/footer/div/div/div[3]/a[4]/i").click()
  assert "https://github.com/centerforopenscience" in driver.current_url
  driver.back()
  #Google plus
  driver.find_element_by_xpath("/html/body/footer/div/div/div[3]/a[5]/i").click()
  assert "https://plus.google.com/104751442909573665859" in driver.current_url
  driver.back()
  
  
  
  
