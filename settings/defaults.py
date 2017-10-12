from selenium import webdriver


USERNAME_ONE = ''

USERNAME_TWO = ''
    
PASSWORD = ''
    
DESIRED_CAP = {'browser': 'Chrome', 'browser_version': '61.0', 'os': 'Windows', 'os_version': '10', 'resolution': '2048x1536'}
    
DRIVER = None

driver_name = 'chrome'

# Default time for WebDriver.implicitly_wait
selenium_wait_time = 5

# Domain to use for all tests.
osf_home = 'https://staging.osf.io'

osf_login_page = 'https://staging-accounts.osf.io/login'