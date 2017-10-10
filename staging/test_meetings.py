import os
import settings
from helpers import login
from helpers import forks
from helpers import nodes
from helpers import meetings
from staging import test_landing_page

#driver = DRIVER
driver = settings.DRIVER
#DRIVER= webdriver.Remote(command_executor, desired_capabilities=DESIRED_CAP)

def test_meetings():
    #login.login(driver)
    test_landing_page.test_landing_page()

