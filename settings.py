import os
from read_env import read_env

# Read .env into os.environ (if it exists)
try:
    read_env()
except FileNotFoundError:
    pass

domains = {
    'stage1': {
        'home': 'https://staging.osf.io',
        'api': 'https://staging-api.osf.io',
        'files': 'https://files.us.staging.osf.io',
        'cas': 'https://accounts.staging.osf.io'
    },
    'stage2': {
        'home': 'https://staging2.osf.io',
        'api': 'https://staging2-api.osf.io',
        'files': 'https://files.us.staging2.osf.io',
        'cas': 'https://accounts.staging2.osf.io'
    },
    'stage3': {
        'home': 'https://staging3.osf.io',
        'api': 'https://staging3-api.osf.io',
        'files': 'https://files.us.staging3.osf.io',
        'cas': 'https://accounts.staging3.osf.io'
    },
    'test': {
        'home': 'https://test.osf.io',
        'api': 'https://test-api.osf.io',
        'files': 'https://files.us.test.osf.io',
        'cas': 'https://accounts.test.osf.io'
    },
    'prod': {
        'home': 'https://osf.io',
        'api': 'https://osf-api.io',
        'files': 'https://files.us.osf.io',
        'cas': 'https://accounts.osf.io'
    }
}

DRIVER = os.environ.get('DRIVER', 'Firefox')
HEADLESS = os.environ.get('HEADLESS', False)

QUICK_TIMEOUT = os.environ.get('QUICK_TIMEOUT', 4)
TIMEOUT = os.environ.get('TIMEOUT', 10)
LONG_TIMEOUT = os.environ.get('LONG_TIMEOUT', 30)

DOMAIN = os.environ.get('DOMAIN', 'stage1')

OSF_HOME = domains[DOMAIN]['home']
API_DOMAIN = domains[DOMAIN]['api']
FILE_DOMAIN = domains[DOMAIN]['files']
CAS_DOMAIN = domains[DOMAIN]['cas']

USER_ONE = os.environ.get('USER_ONE')
USER_ONE_PASSWORD = os.environ.get('USER_ONE_PASSWORD')

# Browser capabilities for browserstack testing
caps = {
    'chrome':
        {'browser': 'Chrome', 'browser_version': '61.0', 'os': 'Windows', 'os_version': '10',
               'resolution': '2048x1536'},
    'edge': {'browser': 'Edge', 'os': 'Windows', 'os_version': '10', 'resolution': '2048x1536'},
    'firefox': {'os': 'OS X', 'os_version': 'Sierra', 'browser': 'Firefox', 'browser_version': '59.0',
                'browserstack.geckodriver': '0.18.0'},
    'msie': {'browser': 'IE', 'browser_version': '11', 'os': 'Windows', 'os_version': '10', 'resolution': '2048x1536'},
    'android': {'device': 'Samsung Galaxy S8', 'realMobile': 'true', 'os_version': '7.0'},
    'ios': {'device': 'iPhone 7', 'realMobile': 'true', 'os_version': '10.0'},
    'safari': {'browser': 'Safari', 'browser_version': '10.1', 'os': 'OS X', 'os_version': 'Sierra',
               'safari.options': {'technologyPreview': 'true'}}
}


# Used for remote testing
if DRIVER == 'Remote':
    BSTACK_USER = os.environ.get('BSTACK_USER')
    BSTACK_KEY = os.environ.get('BSTACK_KEY')

    BUILD = os.environ.get('TEST_BUILD', 'firefox')
    DESIRED_CAP = caps[BUILD]

    upper_build = BUILD.upper()

    USER_ONE = os.environ.get('{}_USER'.format(upper_build), os.environ.get('USER_ONE'))
    USER_ONE_PASSWORD = os.environ.get('{}_USER_PASSWORD'.format(upper_build), os.environ.get('USER_ONE_PASSWORD'))


# Used to skip certain tests on specific stagings
STAGE1 = DOMAIN == 'stage1'
STAGE2 = DOMAIN == 'stage2'
STAGE3 = DOMAIN == 'stage3'
TEST = DOMAIN == 'test'
PRODUCTION = DOMAIN == 'prod'

# TODO: Change to add failsafe but not prohibit
if PRODUCTION:
    raise Exception(
        'OSF UI tests should *never* be run against production. '
        '(A large number of database entries and files are generated '
        'during testing.)'
    )
