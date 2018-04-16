# -*- coding: utf-8 -*-
"""
Base settings file, common to all environments.
These settings can be overridden in local.py.
"""

# Default selenium driver
DRIVER = 'Chrome'


QUICK_TIMEOUT = 4
TIMEOUT = 10
LONG_TIMEOUT = 30

OSF_HOME = 'https://staging.osf.io'
API_DOMAIN = 'https://staging-api.osf.io/v2'
HEADLESS = False
