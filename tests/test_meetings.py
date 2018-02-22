# import pytest

from tests.base import SeleniumTest
from time import sleep
# from api import osf_api as osf

from pages.meetings import MeetingsPage, MeetingDetailPage
from pages.project import ProjectPage


class TestMeetingsPage(SeleniumTest):

    def setup_method(self, method):
        self.meetings_page = MeetingsPage(self.driver)
        self.meetings_page.goto()

    def test_meetings_landing(self):
        assert self.meetings_page.register_text.absent()
        self.meetings_page.register_button.click()
        assert self.meetings_page.register_text.present()

        assert self.meetings_page.upload_text.absent()
        self.meetings_page.upload_button.click()
        assert self.meetings_page.upload_text.present()

        assert self.meetings_page.aps_logo.present()
        assert self.meetings_page.bitss_logo.present()
        assert self.meetings_page.nrao_logo.present()
        assert self.meetings_page.spsp_logo.present()

    def test_meetings_list(self):
        meeting_name = self.meetings_page.top_meeting_link.text
        self.meetings_page.top_meeting_link.click()
        sleep(.1)
        self.driver.switch_to.window(self.driver.window_handles[1])
        meeting_detail = MeetingDetailPage(self.driver)
        assert meeting_name == meeting_detail.meeting_title.text
        self.driver.switch_to.window(self.driver.window_handles[0])

    def test_meeting_detail(self):
        self.meetings_page.top_meeting_link.click()
        sleep(.1)
        self.driver.switch_to.window(self.driver.window_handles[1])
        meeting_detail = MeetingDetailPage(self.driver)
        assert meeting_detail.entry_download_button.present()
        entry_name = meeting_detail.second_entry_link.text
        meeting_detail.second_entry_link.click()
        sleep(.1)
        self.driver.switch_to.window(self.driver.window_handles[2])
        project_page = ProjectPage(self.driver)
        assert entry_name == project_page.project_title.text
        self.driver.switch_to.window(self.driver.window_handles[0])
        # TODO close tabs when test complete instead of navigate back to zero

# Future tests could include:
# - sort carets exist
# - lightly testing sort carets
# - lightly testing filtering
# - click download button, confirm download count increases (this will have to be omitted in production test runs)
