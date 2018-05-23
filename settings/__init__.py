from .defaults import *


try:
    from .local import *  # noqa
except ImportError as error:
    raise ImportError("No local.py settings file found. Did you remember to add your local.py?")

PRODUCTION = '/osf.io' in OSF_HOME

STAGE1 = 'staging.' in OSF_HOME
STAGE2 = 'staging2.' in OSF_HOME
STAGE3 = 'staging3.' in OSF_HOME
TEST = 'test.' in OSF_HOME

# raise an exception if the root domain is production. # TODO: Change to add failsafe but not prohibit
if PRODUCTION:
    raise Exception(
        'OSF UI tests should *never* be run against production. '
        '(A large number of database entries and files are generated '
        'during testing.)'
    )

# make sure there is no trailing slash. TODO: Remove this
OSF_HOME = OSF_HOME.rstrip('/')
