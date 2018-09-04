import pytest

import markers
import settings
from api import osf_api
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

    @markers.smoke_test
    @markers.core_functionality
    def test_change_title(self, project_page, fake):
        new_title = fake.sentence(nb_words=4)
        assert project_page.title.text != new_title
        project_page.title.click()
        project_page.title_input.clear()
        project_page.title_input.send_keys(new_title)
        project_page.title_edit_submit_button.click()
        project_page.verify()  # Wait for the page to reload
        assert project_page.title.text == new_title

    @markers.core_functionality
    def test_log_widget_loads(self, project_page):
        project_page.log_widget.loading_indicator.here_then_gone()
        assert project_page.log_widget.log_items

    @markers.core_functionality
    def test_is_private(self, driver, project_page):
        # Verify that a logged out user cannot see the project
        logout(driver)
        project_page.goto(expect_login_redirect=True)
        login(driver)

    @markers.dont_run_on_prod
    @markers.dont_run_on_preferred_node
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

    @markers.core_functionality
    def test_file_widget_loads(self, project_page_with_file):
        # Check the uploaded file shows up in the files widget
        project_page_with_file.file_widget.loading_indicator.here_then_gone()
        assert project_page_with_file.file_widget.component_and_file_titles[3]

    @markers.smoke_test
    @pytest.mark.skipif(not settings.PREFERRED_NODE, reason='Only run this test if addons are set up on a specific node.')
    def test_addon_files_load(self, project_page, session, driver):
        """This test is very fragile and makes assumptions about your setup.
        You must have all of the addons in `EXPECTED_PROVIDERS` connected to your `PREFERRED_NODE`.
        In each provider you must have a file named `<provider_name>.txt`.

        The test will fail if you do not have the expected providers connected.
        The test will also fail if you have not named your files correctly.
        """
        providers = osf_api.get_node_addons(session, project_page.guid)
        assert set(providers) == set(settings.EXPECTED_PROVIDERS)
        project_page.file_widget.loading_indicator.here_then_gone()
        project_page.file_widget.file_expander.here_then_gone()
        project_page.file_widget.filter_button.click()
        for provider in providers:
            project_page.file_widget.filter_input.clear()
            project_page.file_widget.filter_input.send_keys(provider)
            driver.find_element_by_xpath("//*[contains(text(), '{}')]".format(provider + '.txt'))
