import pytest
import markers
import settings
import logging
import re

from api import osf_api
from utils import find_current_browser
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

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
class TestPreprintWorkflow:

    @markers.dont_run_on_prod
    @markers.core_functionality
    @pytest.mark.usefixtures('delete_user_projects_at_setup')
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

        # Author assertions
        submit_page.public_available_button.click()
        submit_page.public_data_input.click()
        submit_page.public_data_input.send_keys_deliberately('https://osf.io/')
        # Need to scroll down since the Preregistration radio buttons are obscured by the Dev mode warning in test environments
        submit_page.scroll_into_view(submit_page.preregistration_no_button.element)
        submit_page.preregistration_no_button.click()
        submit_page.preregistration_input.click()
        submit_page.preregistration_input.send_keys_deliberately('QA Testing')
        submit_page.save_author_assertions.click()

        submit_page.basics_license_dropdown.click()
        # The order of the options in the license dropdown is not consistent across test environments. So we have to select
        # by the actual text value instead of by relative position (i.e. 3rd option in listbox).
        licenseSelect = Select(submit_page.basics_license_dropdown)
        licenseSelect.select_by_visible_text('CC0 1.0 Universal')
        # Need to scroll down since the Keyword/tags section is obscured by the Dev mode warning in the test environments
        submit_page.scroll_into_view(submit_page.basics_tags_section.element)
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

        submit_page.conflict_of_interest.click()
        submit_page.coi_save_button.click()

        # Wait for Supplemental materials to show
        submit_page.supplemental_create_new_project.click()
        submit_page.supplemental_save_button.click()

        submit_page.create_preprint_button.click()
        submit_page.modal_create_preprint_button.click()

        preprint_detail = PreprintDetailPage(driver, verify=True)
        WebDriverWait(driver, 10).until(EC.visibility_of(preprint_detail.title))

        assert preprint_detail.title.text == project_with_file.title
        match = re.search(r'Supplemental Materials\s+([a-z0-9]{4,8})\.osf\.io/([a-z0-9]{5})', preprint_detail.view_page.text)
        assert match is not None

        # Delete supplemental project created during workflow
        supplemental_guid = match.group(2)
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
        discover_page = PreprintDiscoverPage(driver, provider=provider)

        # This fails only in firefox because of selenium incompatibilities with right-left languages
        if 'firefox' in find_current_browser(driver) and 'arabixiv' in provider['id']:
            discover_page.url_addition += '?q=Analysis'

        discover_page.goto()
        discover_page.verify()
        discover_page.loading_indicator.here_then_gone()

        if osf_api.get_providers_total(provider['attributes']['name'], session=session):
            search_results = discover_page.search_results
            assert search_results
            search_results[0].click()
            PreprintDetailPage(driver, verify=True)
        else:
            assert discover_page.no_results
