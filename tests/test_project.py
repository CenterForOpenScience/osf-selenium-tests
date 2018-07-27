import pytest
import markers

from pages.project import ProjectPage
from pages.login import login, logout

@pytest.fixture()
def project_page(driver, default_project):
    project_page = ProjectPage(driver, guid=default_project.id)
    project_page.goto()
    return project_page

@pytest.fixture()
def project_page_with_file(driver, project_with_file):
    project_page = ProjectPage(driver, guid=project_with_file.id)
    project_page.goto()
    return project_page

@pytest.mark.usefixtures('must_be_logged_in')
class TestProjectDetailPage:

    @markers.core_functionality
    def test_change_title(self, project_page):
        new_title = 'New Day. New Title.'
        assert project_page.title.text != new_title
        project_page.title.click()
        project_page.title_input.clear()
        project_page.title_input.send_keys(new_title)
        project_page.title_edit_submit_button.click()
        assert project_page.title.text == new_title

    @markers.core_functionality
    def test_file_widget_loads(self, project_page_with_file):
        # Check the uploaded file shows up in the files widget
        assert project_page_with_file.file_widget.component_and_file_titles[3]

    @markers.core_functionality
    def test_is_private(self, driver, project_page):
        # Verify that a logged out user cannot see the project
        logout(driver)
        project_page.goto(expect_login_redirect=True)
        login(driver)

    @markers.core_functionality
    def test_make_public(self, driver, project_page):
        # Set project to public
        project_page.make_public_link.click()
        project_page.confirm_privacy_change_link.click()
        assert project_page.make_private_link.present()
        # Confirm logged out user can now see project
        logout(driver)
        project_page.goto()
        login(driver)
