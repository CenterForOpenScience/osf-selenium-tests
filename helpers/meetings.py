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

#CE = os.environ['CE']
#DESIRED_CAP= os.environ['DESIRED_CAP']
#DC = {'browser': 'Chrome', 'browser_version': '61.0', 'os': 'Windows', 'os_version': '10', 'resolution': '2048x1536'}
#DRIVER=webdriver.Remote({CE},desired_capabilities=DC)

def osf_meetings(driver):
    print("sup")
