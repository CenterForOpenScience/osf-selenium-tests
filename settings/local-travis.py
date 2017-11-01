from .defaults import *
import os


os_env = os.environ

USER_ONE = os_env.get('USER_ONE')
USER_ONE_PASSWORD = os_env.get('USER_ONE_PASSWORD')
USER_ONE_TOKEN = os_env.get('USER_ONE_TOKEN')

USER_TWO = os_env.get('USER_TWO')
USER_TWO_PASSWORD = os_env.get('USER_TWO_PASSWORD')
USER_TWO_TOKEN = os_env.get('USER_TWO_TOKEN')

BSTACK_CE = os_env.get('BSTACK_CE')

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
