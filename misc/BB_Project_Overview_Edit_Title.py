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
