'''
Created on Jun 30, 2017

@author: shikhadubey
'''
from selenium import webdriver
from EnableandImportBoxDropboxFigshare import EnableandImport
from EnableandImportGithubGoogleDriveOwnCloudS3 import EnableandImport2



desired_cap = {'browser': 'Firefox', 'browser_version': '55.0 beta', 'os': 'Windows', 'os_version': '7', 'resolution': '1024x768'}

wd= webdriver.Remote(
  command_executor='http://shikhadubey1:Mhtt1XkQq18k8nqQzsqn@hub.browserstack.com:80/wd/hub',
  desired_capabilities= desired_cap)
wd.implicitly_wait(60)

try:
    e= EnableandImport(wd)
    e2= EnableandImport2(wd)
    print("All addons enabled")
    for x in range(0,9):
        wd.find_element_by_partial_link_text("Disconnect").click()
        wd.find_element_by_css_selector("body > div.bootbox.modal.fade.bootbox-confirm.in > div > div > div.modal-footer > button.btn.btn-danger").click()
        
finally:
    print("Done")
