'''
Created on July 3, 2017

@author: patrickanderson
'''
import time

class CreateFork:

    def __init__(self, driver):
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id="projectSubnav"]/div/div[2]/ul/li[6]/a").click()
        time.sleep(3)
        driver.find_element_by_xpath("/html/body/div[3]/div/div[4]/div[2]/div/a").click()
        time.sleep(3)
        driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/button[2]").click()
        time.sleep(5)
        driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/button[2]").click()



# "https://osf.io/twmjs/"