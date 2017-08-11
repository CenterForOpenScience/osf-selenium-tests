from basics.login import Login
from selenium import webdriver

desired_cap = {'browser': 'Chrome', 'browser_version': '59.0', 'os': 'OS X', 'os_version': 'Sierra', 'resolution': '1920x1080'}
driver = webdriver.Remote(
command_executor='http://osfselenium1:9asHrZGoyk7Tesx9agX5@hub.browserstack.com:80/wd/hub',
desired_capabilities=desired_cap)

def test_login():
    l = Login()
    l.staging_login(driver)
    assert driver.find_element_by_xpath("//*[@id='osfHome']/div[3]/div/div/div/div/div[1]/h2")
    driver.quit()