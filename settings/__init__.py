from .defaults import *


try:
    from .local import *  # noqa
except ImportError as error:
    raise ImportError("No local.py settings file found. Did you remember to add your local.py?")

# raise an exception if the root domain is production.
if '/osf.io' in OSF_HOME:
    raise Exception(
        'OSF UI tests should *never* be run against production. '
        '(A large number of database entries and files are generated '
        'during testing.)'
    )

# make sure there is no trailing slash.
OSF_HOME = OSF_HOME.rstrip('/')
