import pytest

import markers
from pages.project import MyProjectsPage, ProjectPage


@pytest.fixture()
def my_projects_page(driver):
    my_projects_page = MyProjectsPage(driver)
    my_projects_page.goto()
    return my_projects_page

@pytest.mark.usefixtures('must_be_logged_in')
class TestMyProjectsPage:

    @markers.dont_run_on_prod
    @markers.core_functionality
    def test_create_new_project(self, driver, my_projects_page, fake):
        title = fake.sentence(nb_words=4)
        my_projects_page.create_project_button.click()
        create_project_modal = my_projects_page.create_project_modal
        create_project_modal.title_input.clear()
        create_project_modal.title_input.send_keys(title)
        create_project_modal.create_project_button.click()
        my_projects_page.project_created_modal.go_to_project_href_link.click()
        project_page = ProjectPage(driver, verify=True)
        assert project_page.title.text == title, 'Project title incorrect.'

    def test_custom_collection(self, default_project, my_projects_page, fake):

        # Create new custom collection
        name = fake.sentence(nb_words=2)
        my_projects_page.create_collection_button.click()
        my_projects_page.create_collection_modal.name_input.click()
        my_projects_page.create_collection_modal.name_input.send_keys(name)
        my_projects_page.create_collection_modal.name_input.click()
        my_projects_page.create_collection_modal.add_button.click()
        my_projects_page.reload()
        assert name in my_projects_page.first_custom_collection.text

        # Add a project to your custom collection
        my_projects_page.first_custom_collection.present()
        my_projects_page.drag_and_drop(my_projects_page.projects[0], my_projects_page.first_custom_collection.element)
        assert '1' in my_projects_page.first_custom_collection.text

        # Delete the custom collection
        my_projects_page.first_collection_settings_button.click()
        my_projects_page.first_collection_remove_button.click()
        my_projects_page.delete_collection_modal.delete_button.click()
        assert my_projects_page.first_custom_collection.present()
