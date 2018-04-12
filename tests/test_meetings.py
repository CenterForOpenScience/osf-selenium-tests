import pytest
import markers

from utils import switch_to_tab
from pages.project import ProjectPage
from pages.meetings import MeetingsPage, MeetingDetailPage


@pytest.fixture
def meetings_page(driver):
    meetings_page = MeetingsPage(driver)
    meetings_page.goto()
    return meetings_page


class TestMeetingsPage:

    def test_meetings_landing(self, meetings_page):
        assert meetings_page.register_text.absent()
        meetings_page.register_button.click()
        assert meetings_page.register_text.present()

        assert meetings_page.upload_text.absent()
        meetings_page.upload_button.click()
        assert meetings_page.upload_text.present()

        assert meetings_page.aps_logo.present()
        assert meetings_page.bitss_logo.present()
        assert meetings_page.nrao_logo.present()
        assert meetings_page.spsp_logo.present()

    def test_filtering(self, meetings_page):
        default_top_result = meetings_page.top_meeting_link.text
        meetings_page.filter_input.clear()
        meetings_page.filter_input.send_keys('j')
        filtered_top_result = meetings_page.top_meeting_link.text
        assert default_top_result != filtered_top_result

    def test_carets(self, meetings_page):
        default_top_result = meetings_page.top_meeting_link.text
        meetings_page.sort_caret_name_desc.click()
        sorted_top_result = meetings_page.top_meeting_link.text
        assert default_top_result != sorted_top_result

    @markers.core_functionality
    def test_meetings_list(self, meetings_page, driver, close_extra_tabs):
        meeting_name = meetings_page.top_meeting_link.text
        meetings_page.top_meeting_link.click()
        switch_to_tab(driver, 1)
        meeting_detail = MeetingDetailPage(driver, verify=True)
        assert meeting_name == meeting_detail.meeting_title.text.strip()


class TestMeetingDetailPage:

    @pytest.fixture
    def meeting_detail_page(self, meetings_page, driver, close_extra_tabs):
        meetings_page.top_meeting_link.click()
        switch_to_tab(driver, 1)
        return MeetingDetailPage(driver, verify=True)

    @markers.core_functionality
    def test_meeting_detail(self, meeting_detail_page, driver):
        assert meeting_detail_page.entry_download_button.present()
        entry_title = meeting_detail_page.second_entry_link.text
        meeting_detail_page.second_entry_link.click()
        switch_to_tab(driver, 2)
        project_page = ProjectPage(driver, verify=True)
        assert entry_title == project_page.project_title.text

    def test_filtering_detail(self, meeting_detail_page):
        default_second_result = meeting_detail_page.second_entry_link.text
        meeting_detail_page.filter_input.clear()
        meeting_detail_page.filter_input.send_keys('q')
        filtered_second_result = meeting_detail_page.second_entry_link.text
        assert default_second_result != filtered_second_result

    def test_carets_detail(self, meeting_detail_page):
        default_second_result = meeting_detail_page.second_entry_link.text
        meeting_detail_page.sort_caret_title_asc.click()
        sorted_second_result = meeting_detail_page.second_entry_link.text
        assert default_second_result != sorted_second_result


# Future tests could include:
# - click download button, confirm download count increases (this will have to be omitted in production test runs)
