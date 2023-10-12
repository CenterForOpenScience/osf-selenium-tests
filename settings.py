from environs import Env


env = Env()
env.read_env()  # Read .env into os.environ, if it exists

domains = {
    'stage1': {
        'home': 'https://staging.osf.io',
        'api': 'https://api.staging.osf.io',
        'files': 'https://files.us.staging.osf.io',
        'cas': 'https://accounts.staging.osf.io',
        'custom_institution_domains': ['https://staging-osf-nd.cos.io'],
    },
    'stage2': {
        'home': 'https://staging2.osf.io',
        'api': 'https://api.staging2.osf.io',
        'files': 'https://files.us.staging2.osf.io',
        'cas': 'https://accounts.staging2.osf.io',
        'custom_institution_domains': [],
    },
    'stage3': {
        'home': 'https://staging3.osf.io',
        'api': 'https://api.staging3.osf.io',
        'files': 'https://files.us.staging3.osf.io',
        'cas': 'https://accounts.staging3.osf.io',
        'custom_institution_domains': [],
    },
    'test': {
        'home': 'https://test.osf.io',
        'api': 'https://api.test.osf.io',
        'files': 'https://files.us.test.osf.io',
        'cas': 'https://accounts.test.osf.io',
        'custom_institution_domains': [],
    },
    'prod': {
        'home': 'https://osf.io',
        'api': 'https://api.osf.io',
        'files': 'https://files.osf.io',
        'cas': 'https://accounts.osf.io',
        'custom_institution_domains': [
            'https://osf.io/institutions/asu',
            'https://osf.io/institutions/bt',
            'https://osf.io/institutions/brown',
            'https://osf.io/institutions/cmu',
            'https://osf.io/institutions/cwru',
            'https://osf.io/institutions/cos',
            'https://osf.io/institutions/cornell',
            'https://osf.io/institutions/duke',
            'https://osf.io/institutions/ecu',
            'https://osf.io/institutions/eur',
            'https://osf.io/institutions/fsu',
            'https://osf.io/institutions/gmu',
            'https://osf.io/institutions/gwu',
            'https://osf.io/institutions/gatech',
            'https://osf.io/institutions/harvard',
            'https://osf.io/institutions/jmu',
            'https://osf.io/institutions/kuleuven',
            'https://osf.io/institutions/mq',
            'https://osf.io/institutions/mit',
            'https://osf.io/institutions/nationalmaglab',
            'https://osf.io/institutions/nesta',
            'https://osf.io/institutions/nyu',
            'https://osf.io/institutions/okstate',
            'https://osf.io/institutions/pu',
            'https://osf.io/institutions/purdue',
            'https://osf.io/institutions/temple',
            'https://osf.io/institutions/thepolicylab',
            'https://osf.io/institutions/ou',
            'https://osf.io/institutions/utdallas',
            'https://osf.io/institutions/theworks',
            'https://osf.io/institutions/tufts',
            'https://osf.io/institutions/ucla',
            'https://osf.io/institutions/ugent',
            'https://osf.io/institutions/ua',
            'https://osf.io/institutions/ubc',
            'https://osf.io/institutions/uct',
            'https://osf.io/institutions/uc',
            'https://osf.io/institutions/colorado',
            'https://osf.io/institutions/edin',
            'https://osf.io/institutions/uol',
            'https://osf.io/institutions/uom',
            'https://osf.io/institutions/umd',
            'https://osf.io/institutions/umb',
            'https://osf.io/institutions/unc',
            'https://osf.io/institutions/nd',
            'https://osf.io/institutions/oxford',
            'https://osf.io/institutions/sc',
            'https://osf.io/institutions/uva',
            'https://osf.io/institutions/vcu',
            'https://osf.io/institutions/vt',
            'https://osf.io/institutions/vua',
            'https://osf.io/institutions/wustl',
            'https://osf.io/institutions/yls',
        ],
    },
}

DRIVER = env('DRIVER', 'Firefox')
HEADLESS = env.bool('HEADLESS', False)

QUICK_TIMEOUT = env.int('QUICK_TIMEOUT', 4)
TIMEOUT = env.int('TIMEOUT', 10)
LONG_TIMEOUT = env.int('LONG_TIMEOUT', 30)
VERY_LONG_TIMEOUT = env.int('VERY_LONG_TIMEOUT', 60)

DOMAIN = env('DOMAIN', 'stage1')

NEW_USER_EMAIL = env('NEW_USER_EMAIL')

# Preferred node must be set to run tests on production
PREFERRED_NODE = env('PREFERRED_NODE', None)
# Initialize Popular Pages environment variable to None which is what it should be for
# all environments except Production which is set below.
POPULAR_PAGES = None
if DOMAIN == 'prod':
    PREFERRED_NODE = env('PREFERRED_NODE')
    # List of popular pages in Production to test as part of the 2 Minute Drill
    POPULAR_PAGES = env.list('POPULAR_PAGES')

EXPECTED_PROVIDERS = env.list(
    'EXPECTED_PROVIDERS',
    [
        'bitbucket',
        'box',
        'dataverse',
        'dropbox',
        'figshare',
        'github',
        'gitlab',
        'googledrive',
        'osfstorage',
        'owncloud',
        'onedrive',
        's3',
    ],
)

OSF_HOME = domains[DOMAIN]['home']
API_DOMAIN = domains[DOMAIN]['api']
FILE_DOMAIN = domains[DOMAIN]['files']
CAS_DOMAIN = domains[DOMAIN]['cas']
CUSTOM_INSTITUTION_DOMAINS = domains[DOMAIN]['custom_institution_domains']

# Browser capabilities for browserstack testing
caps = {
    'chrome': {
        'browser': 'Chrome',
        'os': 'Windows',
        'os_version': '10',
        'resolution': '2048x1536',
    },
    'edge': {
        'browser': 'Edge',
        'os': 'Windows',
        'os_version': '10',
        'resolution': '2048x1536',
    },
    'firefox': {
        'browser': 'Firefox',
        'os': 'Windows',
        'os_version': '10',
        'resolution': '2048x1536',
    },
}

BUILD = DRIVER

if DRIVER == 'Remote':
    BSTACK_USER = env('BSTACK_USER')
    BSTACK_KEY = env('BSTACK_KEY')

    BUILD = env('TEST_BUILD', 'chrome')
    DESIRED_CAP = caps[BUILD]

    upper_build = BUILD.upper()

    USER_ONE = env('{}_USER'.format(upper_build), env('USER_ONE', ''))
    USER_ONE_PASSWORD = env(
        '{}_USER_PASSWORD'.format(upper_build), env('USER_ONE_PASSWORD', '')
    )

    USER_TWO = env('{}_USER_TWO'.format(upper_build), env('USER_TWO', ''))
    USER_TWO_PASSWORD = env(
        '{}_USER_TWO_PASSWORD'.format(upper_build), env('USER_TWO_PASSWORD', '')
    )
else:
    USER_ONE = env('USER_ONE')
    USER_ONE_PASSWORD = env('USER_ONE_PASSWORD')

    USER_TWO = env('USER_TWO')
    USER_TWO_PASSWORD = env('USER_TWO_PASSWORD')


# Used to skip certain tests on specific stagings
STAGE1 = DOMAIN == 'stage1'
STAGE2 = DOMAIN == 'stage2'
STAGE3 = DOMAIN == 'stage3'
TEST = DOMAIN == 'test'
PRODUCTION = DOMAIN == 'prod'

# Users for testing CAS login scemarios
DEACTIVATED_USER = env('DEACTIVATED_USER')
DEACTIVATED_USER_PASSWORD = env('DEACTIVATED_USER_PASSWORD')
UNCONFIRMED_USER = env('UNCONFIRMED_USER')
UNCONFIRMED_USER_PASSWORD = env('UNCONFIRMED_USER_PASSWORD')
CAS_2FA_USER = env('CAS_2FA_USER')
CAS_2FA_USER_PASSWORD = env('CAS_2FA_USER_PASSWORD')
CAS_TOS_USER = env('CAS_TOS_USER')
CAS_TOS_USER_PASSWORD = env('CAS_TOS_USER_PASSWORD')
DEVAPP_CLIENT_ID = env('DEVAPP_CLIENT_ID')
DEVAPP_CLIENT_SECRET = env('DEVAPP_CLIENT_SECRET')

# User with IMAP enabled email
IMAP_EMAIL = env('IMAP_EMAIL')
# Password for IMAP enabled email account - NOT OSF password
IMAP_EMAIL_PASSWORD = env('IMAP_EMAIL_PASSWORD')
IMAP_HOST = env('IMAP_HOST')

REGISTRATIONS_USER = env('REGISTRATIONS_USER')
REGISTRATIONS_USER_PASSWORD = env('REGISTRATIONS_USER_PASSWORD')
