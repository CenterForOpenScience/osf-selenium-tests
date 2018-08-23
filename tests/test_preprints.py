import pytest
import markers
import settings

from api import osf_api

from pages.preprints import (
    PreprintLandingPage,
    PreprintSubmitPage,
    PreprintDetailPage,
    PreprintDiscoverPage,
)


@pytest.fixture
def landing_page(driver):
    landing_page = PreprintLandingPage(driver)
    landing_page.goto()
    return landing_page

#TODO: Add checking for missing translations
@pytest.mark.usefixtures('must_be_logged_in')
@pytest.mark.usefixtures('delete_user_projects_at_setup')
class TestPreprintWorkflow:

    @markers.dont_run_on_prod
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
        preprint_detail = PreprintDetailPage(driver, verify=True)
        assert preprint_detail.title.text == project_with_file.title

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
    """Return the API data of the OSF preprint provider and all preprint providers with custom domains.
    """
    providers = osf_api.get_providers_list()
    return [provider for provider in providers if provider['attributes']['domain_redirect_enabled'] or provider['id'] == 'osf']


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
        PreprintSubmitPage(driver, provider=provider).goto()

    @markers.smoke_test
    @markers.core_functionality
    @pytest.mark.skipif(settings.BUILD == 'msie', reason='Sometimes IE discover page yields no results, see IN-438')
    @pytest.mark.skipif(settings.STAGE1 or settings.STAGE2 or settings.STAGE3, reason='Cannot test on stagings as they share SHARE')
    def test_detail_page(self, driver, provider):
        """Test a preprint detail page by grabbing the first search result from the discover page.
        """
        discover_page = PreprintDiscoverPage(driver, provider=provider)
        discover_page.goto()
        discover_page.loading_indicator.here_then_gone()
        search_results = discover_page.search_results
        assert search_results
        search_results[0].click()
        PreprintDetailPage(driver, verify=True)
