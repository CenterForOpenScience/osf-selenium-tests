from blocks.login import Login
from blocks.variables import Variables

driver = Variables.driver

def test_login():
    Login.login(driver)
    assert driver.find_element_by_xpath("//*[@id='osfHome']/div[3]/div/div/div/div/div[1]/h2")
    driver.quit()