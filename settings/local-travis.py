from .defaults import *
from selenium import webdriver
import os


os_env = os.environ

USERNAME_ONE = os_env.get('USERNAME_ONE')
USERNAME_TWO = os_env.get('USERNAME_TWO')
PASSWORD = os_env.get('PASSWORD')

DRIVER = 'Remote'
DESIRED_CAP = {
    'browser': 'Chrome',
    'browser_version': '61.0',
    'os': 'Windows',
    'os_version': '10',
    'resolution': '2048x1536'
}

OSF_HOME = 'https://staging.osf.io'
API_DOMAIN = 'https://staging-api.osf.io'
