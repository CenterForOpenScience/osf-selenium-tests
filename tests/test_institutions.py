import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import markers
from api import osf_api
from pages.institutions import (
    InstitutionAdminDashboardPage,
    InstitutionBrandedPage,
    InstitutionsLandingPage,
)


@markers.smoke_test
@markers.core_functionality
class TestInstitutionsPage:
    @pytest.fixture()
    def landing_page(self, driver):
        landing_page = InstitutionsLandingPage(driver)
        landing_page.goto()
        return landing_page

    def test_select_institution(self, driver, landing_page):
        landing_page.institution_list[0].click()
        assert InstitutionBrandedPage(driver, verify=True)

    def test_filter_by_institution(
        self, driver, landing_page, institution='Center For Open Science'
    ):
        landing_page.search_bar.send_keys(institution)
        assert institution in landing_page.institution_list[0].text


@markers.dont_run_on_prod
@markers.core_functionality
# Can't run this is Production since we don't have admin access to any institutions in
# Production
class TestInstitutionAdminDashboardPage:
    def test_institution_admin_dashboard(self, driver, session, must_be_logged_in):
        """Test using the COS admin dashboard page - user must already be setup as an
        admin for the COS institution in each environment through the OSF admin app.
        """
        dashboard_page = InstitutionAdminDashboardPage(driver, institution_id='cos')
        dashboard_page.goto()
        assert InstitutionAdminDashboardPage(driver, verify=True)
        dashboard_page.loading_indicator.here_then_gone()

        # Select 'QA' from Departments listbox and verify that the correct number
        # of users are displayed in the table
        dashboard_page.departments_listbox_trigger.click()
        dashboard_page.select_department_from_listbox('QA')
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-test-item-name]'))
        )
        api_qa_users = osf_api.get_institution_users_per_department(
            session, institution_id='cos', department='QA'
        )
        assert len(dashboard_page.user_table_rows) == len(api_qa_users)

        # Get metrics data using the OSF api
        metrics_data = osf_api.get_institution_metrics_summary(
            session, institution_id='cos'
        )
        api_user_count = metrics_data['attributes']['user_count']
        api_public_project_count = metrics_data['attributes']['public_project_count']
        api_private_project_count = metrics_data['attributes']['private_project_count']

        dashboard_page.scroll_into_view(dashboard_page.total_project_count.element)

        # Verify Total User Count
        displayed_user_count = dashboard_page.total_user_count.text
        assert int(displayed_user_count) == api_user_count

        # Verify Public Project Count
        displayed_public_project_count = dashboard_page.public_project_count.text
        assert int(displayed_public_project_count) == api_public_project_count

        # Verify Private Project Count
        displayed_private_project_count = dashboard_page.private_project_count.text
        assert int(displayed_private_project_count) == api_private_project_count

        # Verify Total Project Count
        total_project_count = dashboard_page.total_project_count.text
        assert (
            int(total_project_count)
            == api_public_project_count + api_private_project_count
        )
