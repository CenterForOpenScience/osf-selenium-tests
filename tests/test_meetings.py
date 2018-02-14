import pytest

from tests.base import SeleniumTest
from api import osf_api as osf

from pages.meetings import MeetingsPage


class TestMeetingsPage(SeleniumTest):

    def setup_method(self, method):
        self.meetings_page = MeetingPage(self.driver)
        self.meetings_page.goto()

    def test_meetings_landing(self):
        self.meetings_page.invisible("register_text")
        self.meetings_page.register_button.click()
        self.meetings_page.register_text

        self.meetings_page.invisible("upload_text")
        self.meetings_page.upload_button.click()
        self.meetings_page.upload_text


    # check 4 logos at bottom

    # check clicking a meeting from list and that page loads

    # 2ND TEST (for newly navigated to page) check clicking a meeting project from THAT list and see that project loads
