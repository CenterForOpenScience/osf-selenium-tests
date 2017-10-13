from .defaults import *
from selenium import webdriver
import os


os_env = os.environ

USERNAME_ONE = os_env.get('USERNAME_ONE')
USERNAME_TWO = os_env.get('USERNAME_TWO')
PASSWORD = '"Repr0duce!"'

DRIVER = webdriver.Remote(
    command_executor='http://{}:{}@hub.browserstack.com:80/wd/hub'.format(
        os_env.get('BSTACK_USER'),
        os_env.get('BSTACK_KEY')),
    desired_capabilities=DESIRED_CAP)
