'''
Created on Jun 19, 2017

@author: shikhadubey
'''
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from Login import Login

success= True
class EnableandImport2:
    def is_alert_present(self, wd):
        try:
            wd.switch_to_alert().text
            return True
        except:
            return False
    def __init__(self, wd):
        try:
                                     
            wd.find_element_by_css_selector("input[name=\"github\"]").click()
            time.sleep(3) 
            wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
            time.sleep(3) 
            wd.find_element_by_css_selector("#githubImportToken").click()
            time.sleep(5)
            wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
            time.sleep(3)
            wd.find_element_by_css_selector("#githubSelectRepo > option:nth-child(2)").click()
            time.sleep(3)
            wd.find_element_by_css_selector("#addonSettingsGithub > div.row > div:nth-child(2) > button").click()
            time.sleep(3)
            print("github done")
            wd.find_element_by_css_selector("input[name=\"googledrive\"]").click()
            time.sleep(3) 
            wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
            time.sleep(5) 
            wd.find_element_by_css_selector("#googledriveScope > h4.addon-title > small.authorized-by > span:nth-of-type(2) > a[href=\"#\"].text-primary.pull-right.addon-auth").click()#("/html/body/div[4]/div/div[4]/div[2]/div[3]/div[2]/div[5]/h4/small/span[2]/a").click()
            time.sleep(3)
            wd.find_element_by_xpath("/html/body/div[6]/div/div/div[3]/button[2]").click()
            time.sleep(3)
            wd.find_element_by_css_selector("#tb-tbody > div > div > div:nth-child(2) > div.tb-td.tb-col-1.p-l-xs > input[type=\"radio\"]").click()
            time.sleep(3)
            #clicking save below
            wd.find_element_by_css_selector("#googledriveScope > div.googledrive-settings > div > div > div.m-t-sm.addon-folderpicker-widget.googledrive-widget > div.googledrive-confirm-selection > form > div.pull-right > input").click()
            print("google drive done")
            wd.find_element_by_css_selector("#selectAddonsForm > div:nth-child(10) > label > input").click()
            time.sleep(3)
            wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
            time.sleep(3)
            wd.find_element_by_partial_link_text("Import").click()
            time.sleep(3)
            wd.find_element_by_css_selector("body > div.bootbox.modal.fade.bootbox-confirm.in > div > div > div.modal-footer > button.btn.btn-primary").click()
            time.sleep(7)
            wd.find_element_by_css_selector("#tb-tbody > div > div > div:nth-child(4) > div.tb-td.tb-col-1.p-l-xs > input[type=\"radio\"]").click()  ## Selecting the folder
            time.sleep(3)
            wd.find_element_by_css_selector("#owncloudScope > div.owncloud-settings > div > div > div.m-t-sm.addon-folderpicker-widget.owncloud-widget > div.owncloud-confirm-selection > form > div.pull-right > input").click()
            print("own cloud done")
            time.sleep(3)
            wd.find_element_by_css_selector("input[name=\"s3\"]").click()
            time.sleep(3) 
            wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
            time.sleep(3) 
            wd.find_element_by_partial_link_text("Import").click()
            time.sleep(3)
            wd.find_element_by_css_selector("button[type=\"button\"].btn.btn-primary").click()
            time.sleep(3)
            wd.find_element_by_css_selector("#tb-tbody > div > div > div:nth-child(6) > div.tb-td.tb-col-1.p-l-xs > input[type=\"radio\"]").click()
            time.sleep(3)
            wd.find_element_by_css_selector("#s3Scope > div.s3-settings > div > div > div.m-t-sm.addon-folderpicker-widget.s3-widget > div.s3-confirm-selection > form > div.pull-right > input").click() ## Clicking save
            time.sleep(3)
            print("S3 done")
            wd.find_element_by_css_selector("#selectAddonsForm > div:nth-child(4) > label > input").click()
            time.sleep(3)
            wd.find_element_by_css_selector("body > div.bootbox.modal.fade.bootbox-confirm.in > div > div > div.modal-footer > button.btn.btn-primary").click()
            time.sleep(3)
            wd.find_element_by_partial_link_text("Import").click()
            time.sleep(3)
            wd.find_element_by_css_selector("body > div.bootbox.modal.fade.bootbox-confirm.in > div > div > div.modal-footer > button.btn.btn-primary").click()
            time.sleep(3)
            print("Dataverse done")
            
        
        finally:
            print("getting closer")
            if not success:
                raise Exception("Test failed.")
