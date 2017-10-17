# -*- coding: utf-8 -*-
"""
Base settings file, common to all environments.
These settings can be overridden in local.py.
"""

# Default selenium driver
DRIVER = 'Chrome'

# Default time for WebDriver.implicitly_wait
SEL_WAIT = 5

OSF_HOME = 'http://localhost:5000'
API_DOMAIN = 'http://localhost:8000'
HEADLESS = False
