import re

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import markers
import settings
from api import osf_api
from pages.dashboard import DashboardPage
from pages.institutions import InstitutionsLandingPage
from pages.meetings import MeetingsPage
from pages.preprints import PreprintLandingPage
from pages.project import ProjectPage
from pages.registries import RegistriesLandingPage


@pytest.fixture()
def dashboard_page(driver, must_be_logged_in):
    dashboard_page = DashboardPage(driver)
    dashboard_page.goto()
    return dashboard_page


class TestDashboardPage:
    @markers.dont_run_on_prod
    @markers.core_functionality
    def test_create_project(self, driver, session, dashboard_page):
        title = 'New Project'
        dashboard_page.create_project_button.click()
        create_project_modal = dashboard_page.create_project_modal
        create_project_modal.title_input.clear()
        create_project_modal.title_input.send_keys(title)
        create_project_modal.create_project_button.click()
        # Get guid of newly created project from link on modal
        match = re.search(
            r'([a-z0-9]{4,8})\.osf\.io/([a-z0-9]{5})',
            dashboard_page.project_created_modal.go_to_project_href_link.get_attribute(
                'href'
            ),
        )
        project_guid = match.group(2)
        dashboard_page.project_created_modal.go_to_project_href_link.click()
        project_page = ProjectPage(driver, verify=True)
        assert project_page.title.text == title, 'Project title incorrect.'
        # Delete the project as cleanup
        osf_api.delete_project(session, project_guid, None)

    @markers.core_functionality
    def test_create_project_modal_buttons(self, dashboard_page, session):
        institutions = osf_api.get_user_institutions(session)
        dashboard_page.create_project_button.click()

        create_project_modal = dashboard_page.create_project_modal

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

    @markers.smoke_test
    @markers.core_functionality
    def test_collections_link(self, driver, dashboard_page):
        dashboard_page.collections_link.click()
        # Link opens COS Collections page in new tab, so wait for the second tab to open
        # and switch focus to it.
        WebDriverWait(driver, 3).until(EC.number_of_windows_to_be(2))
        driver.switch_to.window(driver.window_handles[1])
        WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'hs-menu-wrapper'))
        )
        assert 'https://www.cos.io/products/osf-collections' in driver.current_url
        # Close the second tab that was opened. We do not want subsequent tests to use
        # the second tab.
        driver.close()
        # Switch focus back to the first tab
        driver.switch_to.window(driver.window_handles[0])

    @markers.smoke_test
    @markers.core_functionality
    def test_registries_link(self, driver, dashboard_page):
        dashboard_page.registries_link.click()
        RegistriesLandingPage(driver, verify=True)

    @markers.smoke_test
    @markers.core_functionality
    def test_institutions_link(self, driver, dashboard_page):
        dashboard_page.institutions_link.click()
        InstitutionsLandingPage(driver, verify=True)

    @markers.smoke_test
    @markers.core_functionality
    def test_first_preprints_link(self, driver, dashboard_page):
        dashboard_page.preprints_link.click()
        PreprintLandingPage(driver, verify=True)

    # There is some setup involved (not a waffle flag) with getting projects to display in the New and noteworthy
    # section. Currently this only works in the Stage 1 and Stage 3 environments.
    @pytest.mark.skipif(
        settings.STAGE2 or settings.TEST,
        reason='No new and noteworthy node on stage2 or test',
    )
    @markers.smoke_test
    def test_new_and_noteworthy(self, dashboard_page):
        assert dashboard_page.first_noteworthy_project.present()

    # TODO: Maybe add a test to verify Most popular section if/when we ever figure out how a project becomes
    # Most Popular

    @markers.smoke_test
    @markers.core_functionality
    def test_meetings_link(self, driver, dashboard_page):
        dashboard_page.view_meetings_button.click()
        assert MeetingsPage(driver).verify()

    @markers.smoke_test
    @markers.core_functionality
    def test_preprints_link(self, driver, dashboard_page):
        dashboard_page.view_preprints_button.click()
        assert PreprintLandingPage(driver).verify()


@markers.dont_run_on_prod
@pytest.mark.usefixtures('must_be_logged_in')
@pytest.mark.usefixtures('delete_user_projects_at_setup')
class TestProjectList:
    @pytest.fixture()
    def project_one(self, session):
        project_one = osf_api.create_project(session, title='&&aaaaaa')
        yield project_one
        project_one.delete()

    @pytest.fixture()
    def project_two(self, session):
        project_two = osf_api.create_project(session, title='&&aaaabb')
        yield project_two
        project_two.delete()

    @pytest.fixture()
    def project_three(self, session):
        project_three = osf_api.create_project(session, title='&&aaaaac')
        yield project_three
        project_three.delete()

    def test_project_sorting(
        self, driver, dashboard_page, project_one, project_two, project_three
    ):
        dashboard_page.reload()

        project_list = dashboard_page.project_list
        project_list.search_input.clear()
        project_list.search_input.send_keys('&&aaaa')

        assert 'selected' in project_list.sort_date_dsc_button.get_attribute('class')
        assert 'not-selected' in project_list.sort_date_asc_button.get_attribute(
            'class'
        )
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'div[data-test-dashboard-item]')
            )
        )
        assert project_three.id in project_list.get_nth_project_link(1)
        assert project_two.id in project_list.get_nth_project_link(2)
        assert project_one.id in project_list.get_nth_project_link(3)

        project_list.sort_date_asc_button.click()
        assert 'selected' in project_list.sort_date_asc_button.get_attribute('class')
        assert 'not-selected' in project_list.sort_date_dsc_button.get_attribute(
            'class'
        )
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'div[data-test-dashboard-item]')
            )
        )
        assert project_one.id in project_list.get_nth_project_link(1)
        assert project_two.id in project_list.get_nth_project_link(2)
        assert project_three.id in project_list.get_nth_project_link(3)

        project_list.sort_title_asc_button.click()
        assert 'selected' in project_list.sort_title_asc_button.get_attribute('class')
        assert 'not-selected' in project_list.sort_title_dsc_button.get_attribute(
            'class'
        )
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'div[data-test-dashboard-item]')
            )
        )
        assert project_one.id in project_list.get_nth_project_link(1)
        assert project_three.id in project_list.get_nth_project_link(2)
        assert project_two.id in project_list.get_nth_project_link(3)

        project_list.sort_title_dsc_button.click()
        assert 'selected' in project_list.sort_title_dsc_button.get_attribute('class')
        assert 'not-selected' in project_list.sort_title_asc_button.get_attribute(
            'class'
        )
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'div[data-test-dashboard-item]')
            )
        )
        assert project_two.id in project_list.get_nth_project_link(1)
        assert project_three.id in project_list.get_nth_project_link(2)
        assert project_one.id in project_list.get_nth_project_link(3)

    # TODO: Update this test to use more complex characters
    def test_project_quick_search(
        self, driver, dashboard_page, project_one, project_two, project_three
    ):
        dashboard_page.reload()

        project_list = dashboard_page.project_list
        project_list.search_input.clear()
        project_list.search_input.send_keys('&&aaaa')

        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'div[data-test-dashboard-item]')
            )
        )
        assert project_list.get_list_length() == 3

        project_list.search_input.send_keys('a')
        assert project_list.get_list_length() == 2

        project_list.search_input.send_keys('a')
        assert project_list.get_list_length() == 1
        assert project_one.id in project_list.get_nth_project_link(1)
