from .defaults import *
import os

os_env = os.environ

USER_ONE = os_env.get('USER_ONE')
USER_ONE_PASSWORD = os_env.get('USER_ONE_PASSWORD')

USER_TWO = os_env.get('USER_TWO')
USER_TWO_PASSWORD = os_env.get('USER_TWO_PASSWORD')

DRIVER = 'Remote'
DESIRED_CAP = os_env.get('DESIRED_CAP')

OSF_HOME = 'https://staging.osf.io'
API_DOMAIN = 'https://staging-api.osf.io'
