import time
from helpers import login
from utils import launch_driver
import settings


driver = launch_driver()
driver.implicitly_wait(settings.SEL_WAIT)

def test_login():
    login.login(driver)
    assert driver.find_element_by_xpath(
        "//*[@id='osfHome']/div[3]/div/div/div/div/div[1]/h2")
    driver.quit()
