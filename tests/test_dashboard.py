import pytest

from utils import launch_driver, logout
from pages.project import ProjectPage
from pages.dashboard import DashboardPage


class TestDashboardPage:

    @classmethod
    def setup_class(cls):
        cls.driver = launch_driver()

    def teardown_method(self, method):
        logout(self.dashboard_page)

    def setup_method(self, method):
        self.dashboard_page = DashboardPage(self.driver)
        self.dashboard_page.goto()

    def test_create_project(self):
        project_title = 'Totally Unique Project'
        self.dashboard_page.create_project_button.click()
        create_project_modal = self.dashboard_page.CreateProjectModal(self.driver)
        create_project_modal.title_input.send_keys(project_title)
        create_project_modal.create_project_button.click()
        project_created_modal = self.dashboard_page.ProjectCreatedModal(self.driver)
        project_created_modal.go_to_project_button.click()
        project_page = ProjectPage(self.driver, verify=True)
        assert project_page.project_title.text == project_title, "Project title incorrect."

    def test_modal_buttons(self):
        #TODO: Get user institutions from user object
        self.dashboard_page.create_project_button.click()

        create_project_modal = self.dashboard_page.CreateProjectModal(self.driver)

        create_project_modal.more_arrow.click()
        assert create_project_modal.description_input, "Description input missing."
        assert create_project_modal.template_dropdown, "Template dropdown missing."
        create_project_modal.more_arrow.click()
        with pytest.raises(ValueError):
            create_project_modal.description_input
        with pytest.raises(ValueError):
            create_project_modal.template_dropdown

        #TODO: Add back when institutions can be grabbed from user
        # create_project_modal.remove_all_link.click()
        # assert not create_project_modal.institutions_are_selected(institutions)
        # create_project_modal.select_all_link.click()
        # assert create_project_modal.institutions_are_selected(institutions)

        create_project_modal.cancel_button.click()
        with pytest.raises(ValueError):
            create_project_modal.modal

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

