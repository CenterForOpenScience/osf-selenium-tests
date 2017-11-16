import os
from helpers import login
from helpers import forks
from helpers import nodes
from helpers import meetings
from helpers import search
from helpers import search
from helpers import bottom_bar
from utils import launch_driver
import settings


driver = launch_driver()
driver.implicitly_wait(settings.SEL_WAIT)

def test_meetings():
    meetings.osf_meetings_landing_page(driver)
    meetings.osf_meetings_sign_in(driver)
    meetings.osf_meetings_search_meeting(driver)
    driver.get("https://staging.osf.io/meetings/")
    bottom_bar.osf_bottom_bar(driver)
