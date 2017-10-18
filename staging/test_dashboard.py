import unittest

import settings
from helpers import login
from pages import page

# TODO: Create a logout helper
class DashboardPageTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = settings.DRIVER
        login.login(cls.driver)

    def setUp(self):
        self.dashboard_page = page.DashboardPage(self.driver)
        self.dashboard_page.navigate()

    def test_create_project(self):
        project_title = 'Totally Unique Project'
        create_project_modal = self.dashboard_page.click_create_project()
        create_project_modal.set_title(project_title)
        project_created_modal = create_project_modal.click_create_project()
        project_page = project_created_modal.click_go_to_project()
        assert project_page.title_is(project_title), 'Project title incorrect.'

    def test_modal_buttons(self):
        create_project_modal = self.dashboard_page.click_create_project()

        create_project_modal.click_more()
        assert create_project_modal.get_description_input(), 'Description input missing.'
        assert create_project_modal.get_template_dropdown(), 'Template dropdown missing.'
        create_project_modal.click_more()
        assert not create_project_modal.get_description_input(), 'Description input present but not expected.'
        assert not create_project_modal.get_template_dropdown(), 'Template dropdown present but not expected.'

        create_project_modal.click_remove_all_institutions()
        assert not create_project_modal.institutions_selected()
        create_project_modal.click_select_all_institutions()
        assert create_project_modal.institutions_selected()

        create_project_modal.click_cancel()
        assert not create_project_modal.is_present(), 'Create project modal did not exit.'

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main()
