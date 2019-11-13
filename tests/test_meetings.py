import pytest
import markers

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

    def test_filtering(self, meetings_page, driver):
        search_bar = driver.find_element_by_css_selector('div[data-test-meetings-list-search]')
        driver.execute_script('arguments[0].scrollIntoView();', search_bar)
        default_top_result = meetings_page.top_meeting_link.text
        meetings_page.filter_input.clear()
        meetings_page.filter_input.send_keys('z')
        meetings_page = MeetingsPage(driver, verify=True)
        meetings_page.skeleton_row.here_then_gone()

        filtered_top_result = meetings_page.top_meeting_link.text
        assert default_top_result != filtered_top_result

    def test_carets(self, meetings_page, driver):
        search_bar = driver.find_element_by_css_selector('div[data-test-meetings-list-search]')
        driver.execute_script('arguments[0].scrollIntoView();', search_bar)

        default_top_result = meetings_page.top_meeting_link.text
        meetings_page.sort_caret_name_desc.click()
        sorted_top_result = meetings_page.top_meeting_link.text
        assert default_top_result != sorted_top_result

    @markers.core_functionality
    def test_meetings_list(self, meetings_page, driver):
        search_bar = driver.find_element_by_css_selector('div[data-test-meetings-list-search]')
        driver.execute_script('arguments[0].scrollIntoView();', search_bar)

        meeting_name = meetings_page.top_meeting_link.text
        meetings_page.top_meeting_link.click()
        meeting_detail = MeetingDetailPage(driver, verify=True)
        assert meeting_name.strip() == meeting_detail.meeting_title.text.strip()


class TestMeetingDetailPage:

    @pytest.fixture
    def meeting_detail_page(self, meetings_page, driver):
        search_bar = driver.find_element_by_css_selector('div[data-test-meetings-list-search]')
        driver.execute_script('arguments[0].scrollIntoView();', search_bar)

        meetings_page.top_meeting_link.click()
        return MeetingDetailPage(driver, verify=True)

    @markers.core_functionality
    def test_meeting_detail(self, meeting_detail_page, driver):

        assert meeting_detail_page.entry_download_button.present()
        entry_title = meeting_detail_page.first_entry_link.text
        meeting_detail_page.first_entry_link.click()
        project_page = ProjectPage(driver, verify=True)
        assert entry_title.strip() == project_page.title.text

# Future tests could include:
# - click download button, confirm download count increases (this will have to be omitted in production test runs)
