import pytest
import markers

from api import osf_api as osf
from tests.base import SeleniumTest
from pages.project import ProjectPage
from pages.meetings import MeetingsPage
from pages.preprint import PreprintPage
from pages.dashboard import DashboardPage
from pages.prereg import PreregLandingPage


class TestDashboardPage(SeleniumTest):

    def setup_method(self, method):
        self.dashboard_page = DashboardPage(self.driver)
        self.dashboard_page.goto()

    #TODO: Decide if deleting all projects should go somewhere else
    def teardown_method(self, method):
        osf.delete_all_user_projects(session=self.session)

    @markers.core_functionality
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

    def test_create_project_modal_buttons(self):
        institutions = osf.get_user_institutions(self.session)
        self.dashboard_page.create_project_button.click()

        create_project_modal = self.dashboard_page.CreateProjectModal(self.driver)

        if institutions:
            create_project_modal.remove_all_link.click()
            for institution in institutions:
                assert not create_project_modal.institution_selected(institution)
            create_project_modal.select_all_link.click()
            for institution in institutions:
                assert create_project_modal.institution_selected(institution)

        create_project_modal.more_arrow.click()
        assert create_project_modal.description_input, 'Description input missing.'
        assert create_project_modal.template_dropdown, 'Template dropdown missing.'
        create_project_modal.more_arrow.click()
        assert create_project_modal.description_input.absent()
        assert create_project_modal.template_dropdown.absent()

        create_project_modal.cancel_button.click()

        assert create_project_modal.modal.absent()

    def test_institution_logos(self):
        # TODO: This will not work on production - we don't put up all logos
        api_institution_names = osf.get_all_institutions(self.session)
        page_institutions = self.dashboard_page.get_institutions()
        page_institution_names = [i.get_property('name') for i in page_institutions]
        assert set(page_institution_names) == set(api_institution_names)

    def test_new_and_noteworthy(self):
        assert self.dashboard_page.first_popular_project_entry.present()

    def test_meetings_link(self):
        self.dashboard_page.view_meetings_button.click()
        assert MeetingsPage(self.driver).verify()

    def test_preprints_link(self):
        self.dashboard_page.view_preprints_button.click()
        assert PreprintPage(self.driver).verify()

    def test_prereg_link(self):
        self.dashboard_page.start_prereg_button.click()
        assert PreregLandingPage(self.driver).verify()


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

    def test_project_sorting(self, project_one, project_two, project_three):
        self.dashboard_page.reload()

        project_list = self.dashboard_page.ProjectList(self.driver)
        project_list.search_input.clear()
        project_list.search_input.send_keys('&&aaaa')

        assert 'selected' in project_list.sort_date_dsc_button.get_attribute('class')
        assert 'not-selected' in project_list.sort_date_asc_button.get_attribute('class')
        assert project_three.id in project_list.get_nth_project(1)['guid']
        assert project_two.id in project_list.get_nth_project(2)['guid']
        assert project_one.id in project_list.get_nth_project(3)['guid']

        project_list.sort_date_asc_button.click()
        assert 'selected' in project_list.sort_date_asc_button.get_attribute('class')
        assert 'not-selected' in project_list.sort_date_dsc_button.get_attribute('class')
        assert project_one.id in project_list.get_nth_project(1)['guid']
        assert project_two.id in project_list.get_nth_project(2)['guid']
        assert project_three.id in project_list.get_nth_project(3)['guid']

        project_list.sort_title_asc_button.click()
        assert 'selected' in project_list.sort_title_asc_button.get_attribute('class')
        assert 'not-selected' in project_list.sort_title_dsc_button.get_attribute('class')
        assert project_one.id in project_list.get_nth_project(1)['guid']
        assert project_three.id in project_list.get_nth_project(2)['guid']
        assert project_two.id in project_list.get_nth_project(3)['guid']

        project_list.sort_title_dsc_button.click()
        assert 'selected' in project_list.sort_title_dsc_button.get_attribute('class')
        assert 'not-selected' in project_list.sort_title_asc_button.get_attribute('class')
        assert project_two.id in project_list.get_nth_project(1)['guid']
        assert project_three.id in project_list.get_nth_project(2)['guid']
        assert project_one.id in project_list.get_nth_project(3)['guid']

    def test_project_quick_search(self, project_one, project_two, project_three):
        self.dashboard_page.reload()

        project_list = self.dashboard_page.ProjectList(self.driver)

        project_list.search_input.clear()
        project_list.search_input.send_keys('&&aaaa')
        assert project_list.get_list_length() == 3

        project_list.search_input.send_keys('a')
        assert project_list.get_list_length() == 2

        project_list.search_input.send_keys('a')
        assert project_list.get_list_length() == 1
        assert project_one.id in project_list.get_nth_project(1)['guid']
