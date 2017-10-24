import unittest

from utils import launch_driver, login
from pages.dashboard import DashboardPage

class DashboardPageTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = launch_driver()

    def setUp(self):
        self.dashboard_page = DashboardPage(self.driver)
        self.dashboard_page.open()
        login(self.dashboard_page)

    def test_create_project(self):
        project_title = 'Totally Unique Project'
        self.dashboard_page.create_project_button.click()
        create_project_modal = self.dashboard_page.CreateProjectModal(self.driver)
        create_project_modal.title_input.send_keys(project_title)
        create_project_modal.create_project_button.click()
        project_created_modal = self.dashboard_page.ProjectCreatedModal(self.driver)
        project_created_modal.go_to_project_button.click()


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main()
