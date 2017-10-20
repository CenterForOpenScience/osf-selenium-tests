import time
from helpers import login
from utils import launch_driver


driver = launch_driver()

def test_login():
    login.login(driver)
    assert driver.find_element_by_xpath(
        "//*[@id='osfHome']/div[3]/div/div/div/div/div[1]/h2")
    driver.quit()
