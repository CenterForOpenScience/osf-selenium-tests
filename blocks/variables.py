from selenium import webdriver

class Variables:

    username1 = "osframeworktesting+selenium@gmail.com"

    username2 = "osframeworktesting+ghost2@gmail.com"
    
    password = "Repr0duce!"
    
    desired_cap = {'browser': 'Chrome', 'browser_version': '59.0', 'os': 'OS X', 'os_version': 'Sierra', 'resolution': '1920x1080'}
    
    driver = webdriver.Remote(
command_executor='http://osfselenium1:9asHrZGoyk7Tesx9agX5@hub.browserstack.com:80/wd/hub',
desired_capabilities=desired_cap)