import pytest

from tests.base import SeleniumTest
from api import osf_api as osf

from pages.project import ProjectPage
from pages.dashboard import DashboardPage


class TestDashboardPage(SeleniumTest):

    def setup_method(self, method):
        self.dashboard_page = DashboardPage(self.driver)
        self.dashboard_page.goto()

    def test_create_project(self):
        project_title = 'New Project'
        self.dashboard_page.create_project_button.click()
        create_project_modal = self.dashboard_page.CreateProjectModal(self.driver)
        create_project_modal.title_input.clear()
        create_project_modal.title_input.send_keys(project_title)
        create_project_modal.create_project_button.click()
        project_created_modal = self.dashboard_page.ProjectCreatedModal(self.driver)
        project_created_modal.go_to_project_button.click()
        project_page = ProjectPage(self.driver, verify=True)
        assert project_page.project_title.text == project_title, 'Project title incorrect.'

    def test_modal_buttons(self):
        #TODO: Get user institutions from user object
        self.dashboard_page.create_project_button.click()

        create_project_modal = self.dashboard_page.CreateProjectModal(self.driver)

        create_project_modal.more_arrow.click()
        assert create_project_modal.description_input, 'Description input missing.'
        assert create_project_modal.template_dropdown, 'Template dropdown missing.'
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
        create_project_modal.modal

class TestDashboardPageProjectList(SeleniumTest):

    def setup_method(self, method):
        self.dashboard_page = DashboardPage(self.driver)
        self.dashboard_page.goto()

    @pytest.fixture()
    def project_one(self):
        project_one = osf.create_project(self.session, title='&&aaaaaa')
        yield project_one
        project_one.delete()

    @pytest.fixture()
    def project_two(self):
        project_two = osf.create_project(self.session, title='&&aaaabb')
        yield project_two
        project_two.delete()

    @pytest.fixture()
    def project_three(self):
        project_three = osf.create_project(self.session, title='&&aaaaac')
        yield project_three
        project_three.delete()

    def test_sorting(self, project_one, project_two, project_three):
        self.dashboard_page.reload()

        project_list = self.dashboard_page.ProjectList(self.driver)
        project_list.search_input.clear()
        project_list.search_input.send_keys('&&aaaa')

        assert 'selected' in project_list.sort_date_dsc_button.get_attribute('class')
        assert 'not-selected' in project_list.sort_date_asc_button.get_attribute('class')
        assert project_three.id in project_list.get_nth_project(self.driver, 1)['guid']
        assert project_two.id in project_list.get_nth_project(self.driver, 2)['guid']
        assert project_one.id in project_list.get_nth_project(self.driver, 3)['guid']

        project_list.sort_date_asc_button.click()
        assert 'selected' in project_list.sort_date_asc_button.get_attribute('class')
        assert 'not-selected' in project_list.sort_date_dsc_button.get_attribute('class')
        assert project_one.id in project_list.get_nth_project(self.driver, 1)['guid']
        assert project_two.id in project_list.get_nth_project(self.driver, 2)['guid']
        assert project_three.id in project_list.get_nth_project(self.driver, 3)['guid']

        project_list.sort_title_asc_button.click()
        assert 'selected' in project_list.sort_title_asc_button.get_attribute('class')
        assert 'not-selected' in project_list.sort_title_dsc_button.get_attribute('class')
        assert project_one.id in project_list.get_nth_project(self.driver, 1)['guid']
        assert project_three.id in project_list.get_nth_project(self.driver, 2)['guid']
        assert project_two.id in project_list.get_nth_project(self.driver, 3)['guid']

        project_list.sort_title_dsc_button.click()
        assert 'selected' in project_list.sort_title_dsc_button.get_attribute('class')
        assert 'not-selected' in project_list.sort_title_asc_button.get_attribute('class')
        assert project_two.id in project_list.get_nth_project(self.driver, 1)['guid']
        assert project_three.id in project_list.get_nth_project(self.driver, 2)['guid']
        assert project_one.id in project_list.get_nth_project(self.driver, 3)['guid']

    def test_quick_search(self, project_one, project_two, project_three):
        self.dashboard_page.reload()

        project_list = self.dashboard_page.ProjectList(self.driver)

        project_list.search_input.clear()
        project_list.search_input.send_keys('&&aaaa')
        assert project_list.get_list_length(self.driver) == 3

        project_list.search_input.send_keys('a')
        assert project_list.get_list_length(self.driver) == 2

        project_list.search_input.send_keys('a')
        assert project_list.get_list_length(self.driver) == 1
        assert project_one.id in project_list.get_nth_project(self.driver, 1)['guid']
