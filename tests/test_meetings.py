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

    def test_filtering(self):
        default_top_result = self.meetings_page.top_meeting_link.text
        self.meetings_page.filter_input.clear()
        self.meetings_page.filter_input.send_keys('j')
        filtered_top_result = self.meetings_page.top_meeting_link.text
        assert default_top_result != filtered_top_result

    def test_carets(self):
        default_top_result = self.meetings_page.top_meeting_link.text
        self.meetings_page.sort_caret_name_desc.click()
        sorted_top_result = self.meetings_page.top_meeting_link.text
        assert default_top_result != sorted_top_result

    def test_meetings_list(self):
        meeting_name = self.meetings_page.top_meeting_link.text
        self.meetings_page.top_meeting_link.click()
        sleep(.1)
        self.driver.switch_to.window(self.driver.window_handles[1])
        meeting_detail = MeetingDetailPage(self.driver)
        assert meeting_name == meeting_detail.meeting_title.text
        self.driver.switch_to.window(self.driver.window_handles[0])

class TestMeetingDetailPage(SeleniumTest):

    def setup_method(self, method):
        self.meetings_page = MeetingsPage(self.driver)
        self.meetings_page.goto()
        self.meetings_page.top_meeting_link.click()
        sleep(.1)
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.meeting_detail_page = MeetingDetailPage(self.driver)

    def test_meeting_detail(self):
        assert self.meeting_detail_page.entry_download_button.present()
        entry_title = self.meeting_detail_page.second_entry_link.text
        self.meeting_detail_page.second_entry_link.click()
        sleep(.1)
        self.driver.switch_to.window(self.driver.window_handles[2])
        project_page = ProjectPage(self.driver)
        assert entry_title == project_page.project_title.text
        self.driver.switch_to.window(self.driver.window_handles[0])

    def test_filtering_detail(self):
        default_second_result = self.meeting_detail_page.second_entry_link.text
        self.meeting_detail_page.filter_input.clear()
        self.meeting_detail_page.filter_input.send_keys('q')
        filtered_second_result = self.meeting_detail_page.second_entry_link.text
        assert default_second_result != filtered_second_result
        self.driver.switch_to.window(self.driver.window_handles[0])

    def test_carets_detail(self):
        default_second_result = self.meeting_detail_page.second_entry_link.text
        self.meeting_detail_page.sort_caret_title_asc.click()
        sorted_second_result = self.meeting_detail_page.second_entry_link.text
        assert default_second_result != sorted_second_result
        self.driver.switch_to.window(self.driver.window_handles[0])
# TODO close tabs when test complete instead of navigate back to zero

# Future tests could include:
# - click download button, confirm download count increases (this will have to be omitted in production test runs)
