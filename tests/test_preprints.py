import pytest
import markers
from api import osf_api

from pages.preprints import (
    PreprintLandingPage,
    PreprintSubmitPage,
    PreprintDetailPage
)


@pytest.fixture
def landing_page(driver):
    landing_page = PreprintLandingPage(driver)
    landing_page.goto()
    return landing_page

@pytest.fixture
def project_with_file(session, default_project):
    osf_api.upload_fake_file(session, default_project)


@pytest.mark.usefixtures('must_be_logged_in')
@pytest.mark.usefixtures('delete_user_projects_at_setup')
class TestPreprintWorkflow:

    @markers.core_functionality
    def test_create_preprint_from_landing(self, driver, landing_page, project_with_file):
        landing_page.add_preprint_button.click()
        submit_page = PreprintSubmitPage(driver, verify=True)
        submit_page.select_a_service_save_button.click()
        submit_page.upload_from_existing_project_button.click()
        submit_page.upload_project_selector.click()
        submit_page.upload_project_help_text.here_then_gone()
        submit_page.upload_project_selector_project.click()
        submit_page.upload_existing_file_button.click()
        submit_page.upload_select_file.click()
        submit_page.convert_existing_component_button.click()
        submit_page.continue_with_this_project_button.click()
        submit_page.upload_save_button.click()

        submit_page.first_discipline.click()
        submit_page.discipline_save_button.click()

        submit_page.basics_abstract_input.send_keys('Pull an abstract from somewhere. I dont need to have all this plain text in a test. Maybe create a dummy text file for almost everything')
        submit_page.basics_tags_input.send_keys('qatest')
        submit_page.basics_save_button.click()

        submit_page.create_preprint_button.click()
        submit_page.modal_create_preprint_button.click()
        PreprintDetailPage(driver, verify=True)
        # TODO: Make a clean way to check if you are on the correct project
