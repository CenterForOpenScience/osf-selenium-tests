from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

desired_cap = {'browser': 'Chrome', 'browser_version': '59.0', 'os': 'Windows', 'os_version': '10', 'resolution': '1280x1024'}

driver = webdriver.Remote(
    command_executor='http://shikhadubey1:Mhtt1XkQq18k8nqQzsqn@hub.browserstack.com:80/wd/hub',
    desired_capabilities=desired_cap)

user = "shkd28892@yahoo.com"
pwd = "S"

driver.get("https://staging.osf.io/")

driver.find_element_by_xpath("/html/body/div[2]/nav/div/div[2]/ul/li[4]/div/a[2]").click()
inputElement= driver.find_element_by_id("username")
inputElement.send_keys('sdubey@cos.io')

inputElement= driver.find_element_by_id("password")
inputElement.send_keys('Shikh@28892')
#if ( driver.findElement_by_id("rememberMe")).isSelected:
        #{
             #driver.findElement_By_id("rememberMe").click
        #}#
        
inputElement.send_keys(Keys.RETURN)

driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/div/div/div/div[1]/m-b-lg/div/span/button").click()
        #Thread.sleep(6000);
driver.find_element_by_name("projectName").sendKeys("Testselenium")
        #Thread.sleep(4000);
driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/div/div/div/div[1]/m-b-lg/div/span/div/div/div/div[3]/button[2]").click()
        #Thread.sleep(4000);
driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/div/div/div/div[1]/m-b-lg/div/span/div/div/div/div/div[2]/a").click()
print(driver.getTitle())
driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/header/nav/div/div[2]/ul/li[8]/a").click()  #//project settings
       
        
        #Thread.sleep(8000);
driver.find_element_by_xpath("/html/body/div[4]/div/div[4]/div[2]/div[1]/div[2]/button[3]").click() # // Click delete
        #Thread.sleep(6000);
OSNAMES= driver.find_element_by_xpath("/html/body/div[6]/div/div/div[2]/div/p[2]").getText()
parts = OSNAMES.split(" ")
OS = parts[5]
driver.find_element_by_id("bbConfirmText").sendKeys(OS)
        #Thread.sleep(6000);
driver.find_element_by_xpath("/html/body/div[6]/div/div/div[3]/button[2]").click()
#Thread.sleep(6000);
    #logout process
driver.find_element_by_xpath("/html/body/div[2]/nav/div/div[2]/ul/li[5]/a").click() # // settings
      #Thread.sleep(6000);
driver.find_element_by_xpath("/html/body/div[2]/nav/div/div[2]/ul/li[5]/ul/li[4]/a").click()
#Thread.sleep(6000);
driver.quit()

driver.close()

