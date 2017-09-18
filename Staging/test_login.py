import settings
import time
from blocks import login

driver = settings.DRIVER

def test_login():
    login.login(driver)
    time.sleep(5)
    assert driver.find_element_by_xpath("//*[@id='osfHome']/div[3]/div/div/div/div/div[1]/h2")
    driver.quit()