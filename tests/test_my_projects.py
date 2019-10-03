import pytest
import markers
import time

from api import osf_api
from selenium.webdriver import ActionChains
from pages.project import MyProjectsPage, ProjectPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

''' TODO
1 - Edge support
2 - Restructure Test
'''

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

    def test_custom_collection(self, driver, session, default_project, my_projects_page, fake):
        current_browser = driver.desired_capabilities.get('browserName')

        # Create new custom collection
        name = fake.sentence(nb_words=2, variable_nb_words=False)
        my_projects_page.create_collection_button.click()
        my_projects_page.create_collection_modal.name_input.click()
        my_projects_page.create_collection_modal.name_input.send_keys_deliberately(name)
        my_projects_page.create_collection_modal.add_button.click()
        # Wait until modal closes
        WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '#addColl .btn-success')))
        my_projects_page.reload()
        assert name in my_projects_page.first_custom_collection.text

        # Add a project to your custom collection
        my_projects_page.first_custom_collection.present()
        drag_project = my_projects_page.first_project
        drop_collection = my_projects_page.first_custom_collection

        action_chains = ActionChains(driver)
        action_chains.reset_actions()
        # drag_project is a wrapper - use .element to use the WebElement inside it
        action_chains.click_and_hold(drag_project.element).perform()
        # Chrome/Edge -> will highlight multiple rows if you do not sleep here
        time.sleep(1)
        # drop_collection is a wrapper - use .element to use the WebElement inside it
        action_chains.move_to_element(drop_collection.element).perform()
        action_chains.reset_actions()

        if 'chrome' or 'edge' in current_browser:
            action_chains.release().perform()
        # Wait for created collection to have '(1)' in the name
        WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'li[data-index="4"] span'), '(1)'))
        assert '1' in my_projects_page.first_custom_collection.text

        # Delete the custom collection
        my_projects_page.first_collection_settings_button.click()
        my_projects_page.first_collection_remove_button.click()
        my_projects_page.delete_collection_modal.delete_button.click()
        # Wait for danger modal to close
        WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '#removeColl .btn-danger')))
        assert not my_projects_page.first_custom_collection.present()

        guid = my_projects_page.first_project_hyperlink.get_attribute('data-nodeid')
        osf_api.delete_project(session, guid, None)
