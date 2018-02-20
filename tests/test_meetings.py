# import pytest

from tests.base import SeleniumTest
# from api import osf_api as osf

from pages.meetings import MeetingsPage, MeetingDetailPage


class TestMeetingsPage(SeleniumTest):

    def setup_method(self, method):
        self.meetings_page = MeetingsPage(self.driver)
        self.meetings_page.goto()

    def test_meetings_landing(self):
        assert self.meetings_page.register_text.absent()
        self.meetings_page.register_button.click()
        self.meetings_page.register_text

        assert self.meetings_page.upload_text.absent()
        self.meetings_page.upload_button.click()
        self.meetings_page.upload_text

        assert self.meetings_page.aps_logo.present()
        assert self.meetings_page.bitss_logo.present()
        assert self.meetings_page.nrao_logo.present()
        assert self.meetings_page.spsp_logo.present()

    def test_meetings_list(self):
        meeting_name = self.meetings_page.top_meeting_link.text
        self.meetings_page.top_meeting_link.click()
        meeting_detail = MeetingDetailPage(self.driver)
        assert self.meetings_page.upload_text.absent()
        self.driver.switch_to.window(self.driver.window_handles[1])
        assert meeting_name == meeting_detail.meeting_title.text

    # Note for future tests: add 2nd test for a meetings detail page and clicking an individual meeting from that list
