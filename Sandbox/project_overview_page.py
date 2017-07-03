from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
import unittest, time, re

desired_cap = {'browser': 'Safari', 'browser_version': '10.0', 'os': 'OS X', 'os_version': 'Sierra', 'resolution': '1024x768'}

class DuplicateButtonForkTest(unittest.TestCase):
    def setUp(self):
        url = 'http://allisonschiller1:YcvmHyZcMT9WBrvzzhxT@hub.browserstack.com:80/wd/hub'
        self.driver = webdriver.Remote(command_executor=url,
        desired_capabilities=desired_cap)
        self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_fork(self):
        driver = self.driver
        driver.get('https://staging.osf.io/')
        driver.find_element_by_link_text("Sign In").click()
        driver.implicitly_wait(30)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("\"Repr0duce!\"")
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("osframeworktesting+ghost@gmail.com")
        driver.find_element_by_name("submit").click()
        time.sleep(5)
        driver.get('https://staging.osf.io/dgtc6/')
        # Navigates to "Fork Project"
        driver.implicitly_wait(30)
        driver.find_element_by_css_selector('i.fa.fa-code-fork').click()
        # Clicks duplicate button
        time.sleep(3)
        driver.find_element_by_xpath("//*[contains(text(), 'Fork this Project')]").click()
        # Clicks "Fork this Project" in dropdown
        time.sleep(3)
        driver.find_element_by_xpath("//button[contains(text(), 'Fork')]").click()
        # Clicks "Fork" in "Are you sure you want to fork this project?" modal
        time.sleep(3)
        driver.find_element_by_xpath("//*[contains(text(), 'Go to new fork')]").click()
        # Clicks "Go to new fork" button in modal
        time.sleep(5)
        element = driver.find_element_by_id('nodeTitleEditable')
        # Locates title
        assert element.text == 'Fork of Fork Project'
        # Confirms title reads: "Fork of Fork Project"

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
  unittest.main()
