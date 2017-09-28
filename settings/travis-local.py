from .defaults import *
from selenium import webdriver


USERNAME_ONE = "osframeworktesting+selenium@gmail.com"

USERNAME_TWO = "osframeworktesting+ghost2@gmail.com"
   
PASSWORD = '"Repr0duce!"'
        
DRIVER = webdriver.Remote(
command_executor='http://osfselenium1:9asHrZGoyk7Tesx9agX5@hub.browserstack.com:80/wd/hub',
desired_capabilities=DESIRED_CAP)
