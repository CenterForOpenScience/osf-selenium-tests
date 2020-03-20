import pytest
import markers
import settings
import logging

from api import osf_api
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.preprints import (
    PreprintLandingPage,
    PreprintSubmitPage,
    PreprintDetailPage,
    PreprintDiscoverPage,
)

logger = logging.getLogger(__name__)


@pytest.fixture
def landing_page(driver):
    landing_page = PreprintLandingPage(driver)
    landing_page.goto()
    return landing_page

# TODO: Add checking for missing translations
@pytest.mark.usefixtures('must_be_logged_in')
@pytest.mark.usefixtures('delete_user_projects_at_setup')
class TestPreprintWorkflow:

    @markers.dont_run_on_prod
    @markers.core_functionality
    def test_create_preprint_from_landing(self, session, driver, landing_page, project_with_file):

        landing_page.add_preprint_button.click()
        submit_page = PreprintSubmitPage(driver, verify=True)

        # Wait for select a service to show
        WebDriverWait(driver, 10).until(EC.visibility_of(submit_page.select_a_service_help_text))
        submit_page.select_a_service_save_button.click()
        submit_page.upload_from_existing_project_button.click()
        submit_page.upload_project_selector.click()
        submit_page.upload_project_help_text.here_then_gone()
        submit_page.upload_project_selector_project.click()

        submit_page.upload_select_file.click()
        submit_page.upload_file_save_continue.click()

        submit_page.basics_license_dropdown.click()
        submit_page.basics_universal_license.click()
        submit_page.basics_tags_section.click()
        submit_page.basics_tags_input.send_keys('selenium\r')
        submit_page.basics_abstract_input.click()
        submit_page.basics_abstract_input.send_keys('Center for Open Selenium')
        submit_page.basics_save_button.click()

        # Wait for discipline help text
        submit_page.first_discipline.click()
        submit_page.discipline_save_button.click()

        # Wait for authors box to show
        submit_page.authors_save_button.click()

        # Wait for Supplemental materials to show
        submit_page.supplemental_create_new_project.click()
        submit_page.supplemental_save_button.click()

        submit_page.create_preprint_button.click()
        submit_page.modal_create_preprint_button.click()

        current_browser = driver.desired_capabilities.get('browserName')
        if 'edge' in current_browser:
            alert = driver.switch_to_alert()
            alert.accept()

        preprint_detail = PreprintDetailPage(driver, verify=True)
        WebDriverWait(driver, 10).until(EC.visibility_of(preprint_detail.title))

        assert preprint_detail.title.text == project_with_file.title

        # Delete supplemental project created during workflow
        supplemental_guid = preprint_detail.supplemental_link.text[12:17]
        osf_api.delete_project(session, supplemental_guid, None)

    @markers.smoke_test
    @markers.core_functionality
    def test_search_results_exist(self, driver, landing_page):
        landing_page.search_button.click()
        discover_page = PreprintDiscoverPage(driver, verify=True)
        discover_page.loading_indicator.here_then_gone()
        assert len(discover_page.search_results) > 0


@pytest.fixture(scope='session')
def providers():
    """Return all preprint providers.
    """
    return osf_api.get_providers_list()


@pytest.fixture(scope='session')
def custom_providers():
    """Return the API data of all preprint providers with custom domains.
    """
    providers = osf_api.get_providers_list()
    return [provider for provider in providers if provider['attributes']['domain_redirect_enabled']]


class TestBrandedProviders:

    @pytest.fixture(params=custom_providers(), ids=[prov['id'] for prov in custom_providers()])
    def provider(self, request):
        return request.param

    def test_landing_page_loads(self, driver, provider):
        PreprintLandingPage(driver, provider=provider).goto()

    def test_discover_page_loads(self, driver, provider):
        PreprintDiscoverPage(driver, provider=provider).goto()

    @pytest.mark.usefixtures('must_be_logged_in')
    def test_submit_page_loads(self, driver, provider):
        allow_submissions = osf_api.get_provider_submission_status(provider)
        if allow_submissions:
            PreprintSubmitPage(driver, provider=provider).goto()
        else:
            landing_page = PreprintLandingPage(driver, provider=provider)
            landing_page.goto()
            assert 'submit' not in landing_page.submit_navbar.text
            assert not landing_page.submit_button.present()

    @markers.smoke_test
    @markers.core_functionality
    @pytest.mark.skipif(not settings.PRODUCTION, reason='Cannot test on stagings as they share SHARE')
    def test_detail_page(self, session, driver, provider):
        """Test a preprint detail page by grabbing the first search result from the discover page.
        """
        if osf_api.get_providers_total(provider['attributes']['name'], session=session):
            discover_page = PreprintDiscoverPage(driver, provider=provider)
            discover_page.goto()
            discover_page.verify()
            discover_page.loading_indicator.here_then_gone()
            search_results = discover_page.search_results
            assert search_results
            search_results[0].click()
            PreprintDetailPage(driver, verify=True)
