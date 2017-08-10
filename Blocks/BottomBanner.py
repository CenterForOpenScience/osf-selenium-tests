'''
This module:
1. Goes to the staging.osf.io
2. Checks if the page contains: Copyright 2011
3. The Center for Open Science link is present and opens 'cos.io' when clicked
4. The Terms and Conditions link is present and opens to the terms and conditions link on github when it is clicked
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


desired_cap = {'browser': 'Firefox', 'browser_version': '55.0 beta', 'os': 'Windows', 'os_version': '7', 'resolution': '1024x768'}

wd= webdriver.Remote(
  command_executor='http://shikhadubey1:Mhtt1XkQq18k8nqQzsqn@hub.browserstack.com:80/wd/hub',
  desired_capabilities= desired_cap)
wd.implicitly_wait(60)

try:
    wd.get("https://staging.osf.io/")
    pagesource= (wd.page_source)
    if pagesource.find("Copyright 2011"):
        print("The bottom banner contains Copyright 2011")
    
    link= wd.find_element_by_xpath("//*[contains(text(), 'Center for Open Science')]")
    link.click()
    curre = wd.current_url
    print(curre)
    if curre== 'https://cos.io/':
        print("The COS link works good")
        time.sleep(3)
    wd.back()
    time.sleep(3)
    link= wd.find_element_by_partial_link_text("Terms of Use")
    link.click()
    curre= wd.current_url
    if curre== 'https://github.com/CenterForOpenScience/cos.io/blob/master/TERMS_OF_USE.md':
        print("Terms of use links is good")
        time.sleep(3)
    wd.back()
    time.sleep(3)
    link= wd.find_element_by_xpath("//*[contains(text(), 'Privacy Policy')]")
    link.click()
    curre = wd.current_url
    print(curre)
    if curre== 'https://github.com/CenterForOpenScience/cos.io/blob/master/PRIVACY_POLICY.md':
        print("privacy policy link works good")
        time.sleep(3)
    

finally:
    print("Done")
