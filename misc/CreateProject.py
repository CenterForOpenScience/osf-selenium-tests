'''
Created on Jun 14, 2017

@author: shikhadubey
'''
import time#

class CreateProject:

    def __init__(self, driver):
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id='osfHome']/div[2]/div/div/div/div/div[1]/m-b-lg/div/span/button").click()
        time.sleep(3)
        driver.find_element_by_name("projectName").send_keys("Testselenium")
        driver.find_element_by_xpath("//*[@id='addProjectFromHome']/div/div/div[3]/button[2]").click()
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id='addProjectFromHome']/div/div/div/div[2]/a").click()
        