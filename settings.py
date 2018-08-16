from environs import Env
env = Env()
env.read_env()  # Read .env into os.environ, if it exists

domains = {
    'stage1': {
        'home': 'https://staging.osf.io',
        'api': 'https://api.staging.osf.io',
        'files': 'https://files.us.staging.osf.io',
        'cas': 'https://accounts.staging.osf.io'
    },
    'stage2': {
        'home': 'https://staging2.osf.io',
        'api': 'https://api.staging2.osf.io',
        'files': 'https://files.us.staging2.osf.io',
        'cas': 'https://accounts.staging2.osf.io'
    },
    'stage3': {
        'home': 'https://staging3.osf.io',
        'api': 'https://api.staging3.osf.io',
        'files': 'https://files.us.staging3.osf.io',
        'cas': 'https://accounts.staging3.osf.io'
    },
    'test': {
        'home': 'https://test.osf.io',
        'api': 'https://api.test.osf.io',
        'files': 'https://files.us.test.osf.io',
        'cas': 'https://accounts.test.osf.io'
    },
    'prod': {
        'home': 'https://osf.io',
        'api': 'https://api.osf.io',
        'files': 'https://files.osf.io',
        'cas': 'https://accounts.osf.io'
    }
}

DRIVER = env('DRIVER', 'Firefox')
HEADLESS = env.bool('HEADLESS', False)

QUICK_TIMEOUT = env.int('QUICK_TIMEOUT', 4)
TIMEOUT = env.int('TIMEOUT', 10)
LONG_TIMEOUT = env.int('LONG_TIMEOUT', 30)

DOMAIN = env('DOMAIN', 'stage1')

# Preferred node must be set to run tests on production
PREFERRED_NODE = env('PREFERRED_NODE', None)
if DOMAIN == 'prod':
    PREFERRED_NODE = env('PREFERRED_NODE')

OSF_HOME = domains[DOMAIN]['home']
API_DOMAIN = domains[DOMAIN]['api']
FILE_DOMAIN = domains[DOMAIN]['files']
CAS_DOMAIN = domains[DOMAIN]['cas']

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

if DRIVER == 'Remote':
    BSTACK_USER = env('BSTACK_USER')
    BSTACK_KEY = env('BSTACK_KEY')

    BUILD = env('TEST_BUILD', 'chrome')
    DESIRED_CAP = caps[BUILD]

    upper_build = BUILD.upper()

    USER_ONE = env('{}_USER'.format(upper_build), env('USER_ONE', ''))
    USER_ONE_PASSWORD = env('{}_USER_PASSWORD'.format(upper_build), env('USER_ONE_PASSWORD', ''))
else:
    USER_ONE = env('USER_ONE')
    USER_ONE_PASSWORD = env('USER_ONE_PASSWORD')


# Used to skip certain tests on specific stagings
STAGE1 = DOMAIN == 'stage1'
STAGE2 = DOMAIN == 'stage2'
STAGE3 = DOMAIN == 'stage3'
TEST = DOMAIN == 'test'
PRODUCTION = DOMAIN == 'prod'
