import pytest
from pages.meetings import MeetingsPage


@pytest.fixture()
def meetings_page(driver):
    meetings_page = MeetingsPage(driver)
    meetings_page.goto()
    return meetings_page

class TestMeetingsPage:

    def test_meetings_landing(self, meetings_page):
        meetings_page.register_text.absent()
        meetings_page.register_button.click()
        meetings_page.register_text

        meetings_page.upload_text.absent()
        meetings_page.upload_button.click()
        meetings_page.upload_text

    # check 4 logos at bottom

    # check clicking a meeting from list and that page loads

    # 2ND TEST (for newly navigated to page) check clicking a meeting project from THAT list and see that project loads
