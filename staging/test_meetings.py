import os
import settings
from helpers import login
from helpers import forks
from helpers import nodes
from helpers import meetings
from helpers import search

#driver = DRIVER
driver = settings.DRIVER
#DRIVER= webdriver.Remote(command_executor, desired_capabilities=DESIRED_CAP)

def test_meetings():
    #login.login(driver)
    search.staging_navbar(driver)

