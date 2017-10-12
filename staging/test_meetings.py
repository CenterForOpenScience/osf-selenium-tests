import os
import settings
from helpers import login
from helpers import forks
from helpers import nodes
from helpers import meetings
from helpers import search
from helpers import search

#driver = DRIVER
driver = settings.DRIVER
#DRIVER= webdriver.Remote(command_executor, desired_capabilities=DESIRED_CAP)

def test_meetings():
    meetings.osf_meetings_landing_page(driver)
    meetings.osf_meetings_sign_in(driver)
    meetings.osf_meetings_search_meeting(driver)
    meetings.osf_meeting_bottom_bar(driver)
    
