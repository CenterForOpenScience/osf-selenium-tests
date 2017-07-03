from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

desired_cap = {'browser': 'Safari', 'browser_version': '10.0', 'os': 'OS X', 'os_version': 'Sierra', 'resolution': '1024x768'}

driver = webdriver.Remote(
command_executor='http://amandacos1:mvVRhGj3TDkmxLfKaXUT@hub.browserstack.com:80/wd/hub',
desired_capabilities=desired_cap)
driver.get('https://staging.osf.io/')
driver.find_element_by_link_text("Sign In").click()
driver.implicitly_wait(30)
driver.find_element_by_id("password").clear()
driver.find_element_by_id("password").send_keys("\"Repr0duce!\"")
driver.find_element_by_id("username").clear()
driver.find_element_by_id("username").send_keys("osframeworktesting+ghost@gmail.com")
driver.find_element_by_name("submit").click()

success = True
wd = driver
time.sleep(3)

def is_alert_present(wd):
    try:
        wd.switch_to_alert().text
        return True
    except:
        return False

try:
    wd.get("https://staging.osf.io/qze76/")
    new_title = "Brave New Title"
    wd.find_element_by_css_selector("#nodeTitleEditable").click()
    wd.implicitly_wait(30)
    wd.find_element_by_class_name("editable-clear-x").click()
    time.sleep(1)
    wd.find_element_by_css_selector(".node-title input").send_keys(str(new_title))
    time.sleep(1)
    wd.find_element_by_css_selector("button.editable-cancel").click()
    if wd.find_element_by_css_selector("#nodeTitleEditable").text != "Test Project":
        raise Exception("not assertText failed")
    wd.find_element_by_css_selector("#nodeTitleEditable").click()
    wd.find_element_by_css_selector(".node-title input").click()
    wd.find_element_by_css_selector(".node-title input").clear()
    wd.find_element_by_css_selector(".node-title input").send_keys(str(new_title))
    wd.find_element_by_css_selector("button.editable-submit").click()
    if wd.find_element_by_css_selector("#nodeTitleEditable").text != str(new_title):
        raise Exception("not assertText failed")
finally:
    wd.quit()
    if not success:
        raise Exception("Test failed.")
