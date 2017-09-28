from .defaults import *
from selenium import webdriver


travis encrypt USERNAME_ONE = "osframeworktesting+selenium@gmail.com"

travis encrypt USERNAME_TWO = "osframeworktesting+ghost2@gmail.com"
   
travis encrypt PASSWORD = '"Repr0duce!"'
        
travis encrypt DRIVER = webdriver.Remote(
command_executor='http://osfselenium1:9asHrZGoyk7Tesx9agX5@hub.browserstack.com:80/wd/hub',
desired_capabilities=DESIRED_CAP)
