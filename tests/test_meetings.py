import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import markers
from pages.meetings import (
    MeetingDetailPage,
    MeetingsPage,
)
from pages.project import ProjectPage


@pytest.fixture
def meetings_page(driver):
    meetings_page = MeetingsPage(driver)
    meetings_page.goto_with_reload()
    return meetings_page


@markers.smoke_test
@markers.core_functionality
class TestMeetingsPage:
    def test_meetings_landing(self, meetings_page, driver):
        assert meetings_page.register_text.absent()
        # Need to scroll down since the Register button is obscured by the Dev mode warning in staging environments
        # Targeting the text about the conference minimum to scroll to since it is under the Register button and so
        # the scroll should put the Register button in the middle of the page.
        conference_text = driver.find_element_by_css_selector(
            '[data-test-meetings-list-min-5]'
        )
        meetings_page.scroll_into_view(conference_text)
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
        search_bar = driver.find_element_by_css_selector(
            'div[data-test-meetings-list-search]'
        )
        driver.execute_script('arguments[0].scrollIntoView();', search_bar)
        default_top_result = meetings_page.top_meeting_link.text
        meetings_page.filter_input.clear()
        meetings_page.filter_input.send_keys('z')
        meetings_page = MeetingsPage(driver, verify=True)
        meetings_page.skeleton_row.here_then_gone()

        filtered_top_result = meetings_page.top_meeting_link.text
        assert default_top_result != filtered_top_result

    def test_carets(self, meetings_page, driver):
        search_bar = driver.find_element_by_css_selector(
            'div[data-test-meetings-list-search]'
        )
        driver.execute_script('arguments[0].scrollIntoView();', search_bar)

        default_top_result = meetings_page.top_meeting_link.text
        meetings_page.sort_caret_name_desc.click()
        sorted_top_result = meetings_page.top_meeting_link.text
        assert default_top_result != sorted_top_result

    def test_meetings_list(self, meetings_page, driver):
        search_bar = driver.find_element_by_css_selector(
            'div[data-test-meetings-list-search]'
        )
        driver.execute_script('arguments[0].scrollIntoView();', search_bar)

        meeting_name = meetings_page.top_meeting_link.text
        meetings_page.top_meeting_link.click()
        meeting_detail = MeetingDetailPage(driver, verify=True)
        assert meeting_name.strip() == meeting_detail.meeting_title.text.strip()


@markers.smoke_test
@markers.core_functionality
class TestMeetingDetailPage:
    @pytest.fixture
    def meeting_detail_page(self, meetings_page, driver):
        search_bar = driver.find_element_by_css_selector(
            'div[data-test-meetings-list-search]'
        )
        driver.execute_script('arguments[0].scrollIntoView();', search_bar)

        meetings_page.top_meeting_link.click()
        return MeetingDetailPage(driver, verify=True)

    def test_meeting_detail(self, meeting_detail_page, driver):

        assert meeting_detail_page.entry_download_button.present()
        entry_title = meeting_detail_page.first_entry_link.text
        # Need to scroll down since the first entry link is obscured by the Dev mode
        # warning in staging environments and need to use second project entry to scroll
        # to since scrolling to first entry sometimes still leaves it  partially obscured
        # in some environments (stage 1).
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'li._list-group-item_8wsr4d:nth-child(2)')
            )
        )
        second_entry = driver.find_element_by_css_selector(
            'li._list-group-item_8wsr4d:nth-child(2) > div:nth-child(2)'
        )
        meeting_detail_page.scroll_into_view(second_entry)
        meeting_detail_page.first_entry_link.click()
        project_page = ProjectPage(driver, verify=True)
        assert entry_title.strip() == project_page.title.text


# Future tests could include:
# - click download button, confirm download count increases (this will have to be omitted in production test runs)
