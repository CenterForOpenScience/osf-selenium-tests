import pytest
import markers
import time

from api import osf_api
from selenium.webdriver import ActionChains
from pages.project import MyProjectsPage, ProjectPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture()
def my_projects_page(driver):
    my_projects_page = MyProjectsPage(driver)
    my_projects_page.goto()
    return my_projects_page


@pytest.mark.skip(reason='Skip this test until bug ticket ENG-1737 is resolved')
@pytest.mark.usefixtures('must_be_logged_in')
class TestMyProjectsPage:
    """ Custom collections must implement a PRE-delete setup to start in a clean state.
    """
    @markers.dont_run_on_prod
    @markers.core_functionality
    def test_create_new_project(self, driver, session, my_projects_page, fake):
        title = fake.sentence(nb_words=4)
        my_projects_page.create_project_button.click()
        create_project_modal = my_projects_page.create_project_modal
        create_project_modal.title_input.clear()
        create_project_modal.title_input.send_keys(title)
        create_project_modal.create_project_button.click()
        my_projects_page.project_created_modal.keep_working_here_button.click()

        # Wait until modal is gone
        WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'button[data-dismiss="modal"]')))
        my_projects_page.goto()
        guid = my_projects_page.first_project_hyperlink.get_attribute('data-nodeid')
        my_projects_page.first_project_hyperlink.click()

        # Test & Cleanup
        project_page = ProjectPage(driver, verify=True)
        assert project_page.title.text == title, 'Project title incorrect.'
        osf_api.delete_project(session, guid, None)

    def test_create_custom_collection(self, driver, session, default_project, my_projects_page, fake):
        current_browser = driver.desired_capabilities.get('browserName')

        osf_api.delete_custom_collections(session)

        # Create new custom collection
        name = fake.sentence(nb_words=2, variable_nb_words=False)
        my_projects_page.create_collection_button.click()
        my_projects_page.create_collection_modal.name_input.click()
        my_projects_page.create_collection_modal.name_input.send_keys_deliberately(name)
        my_projects_page.create_collection_modal.add_button.click()

        # Wait until modal closes, then test for presence
        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '#addColl .btn-success')))
        my_projects_page.reload()
        assert name in my_projects_page.first_custom_collection.text

        # Add a project to your custom collection
        my_projects_page.first_custom_collection.present()
        drag_project = my_projects_page.first_project
        drop_collection = my_projects_page.first_custom_collection

        action_chains = ActionChains(driver)
        # drag_project is a wrapper - use .element to use the WebElement inside it
        # drop_collection is a wrapper - use .element to use the WebElement inside it
        if 'firefox' in current_browser:
            action_chains.drag_and_drop(drag_project.element, drop_collection.element)
            action_chains.perform()
        else:
            action_chains.click_and_hold(drag_project.element).perform()
            # Chrome -> will highlight multiple rows if you do not sleep here
            time.sleep(1)
            action_chains.move_to_element(drop_collection.element).perform()
            action_chains.reset_actions()
            action_chains.click_and_hold(drag_project.element)
            action_chains.move_to_element(drop_collection.element).perform()
            action_chains.reset_actions()
            action_chains.release().perform()

        # Wait for new collection to have '(1)' in the name
        WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'li[data-index="4"] span'), '(1)'))
        assert '1' in my_projects_page.first_custom_collection.text

    def test_delete_custom_collection(self, session, driver, my_projects_page):
        # API Setup
        osf_api.delete_custom_collections(session)
        osf_api.create_custom_collection(session)

        my_projects_page.goto()
        assert my_projects_page.first_custom_collection.text

        # Delete the custom collection
        my_projects_page.first_collection_settings_button.click()
        my_projects_page.first_collection_remove_button.click()
        my_projects_page.delete_collection_modal.delete_button.click()

        # Wait for danger modal to close
        WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '#removeColl .btn-danger')))
        assert not my_projects_page.first_custom_collection.present()
