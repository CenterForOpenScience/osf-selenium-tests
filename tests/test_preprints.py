import pytest
import markers
import settings
import logging
import re
import os

from api import osf_api
from utils import find_current_browser
from datetime import datetime
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By

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

    @pytest.fixture()
    def preprint_project(self, session):
        now = datetime.now()
        dtStamp = now.strftime('%m%d%Y-%H%M%S')
        preprintTitle = 'OSF Test Preprint created on ' + dtStamp
        tags = ['preprint test', os.environ['PYTEST_CURRENT_TEST']]
        preprint_project = osf_api.create_project(session, title=preprintTitle, tags=tags)
        osf_api.upload_fake_file(session, preprint_project)
        yield preprint_project
        preprint_project.delete()

    @markers.dont_run_on_prod
    @markers.core_functionality
    @pytest.mark.usefixtures('delete_user_projects_at_setup')
    def test_create_preprint_from_landing(self, session, driver, landing_page, preprint_project):

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

        # Author Assertions section:
        # Note: We can't use the submit_page.save_author_assertions object here, because it is disabled and any time we use
        # an object defined in pages/preprints.py it uses get_web_element() in the Locator class.  Within get_web_element() the
        # element_to_be_clickable method is used, and this method will always fail for disabled objects.  So in this instance
        # we have to get the button object using the driver.find_element method while it is disabled.  After the button becomes
        # enabled (i.e. after required data has been provided) then we can use the submit_page.save_author_assertions object to
        # check the disabled property.  See implementation below.
        assert driver.find_element(By.CSS_SELECTOR, '[data-test-author-assertions-continue]').get_property('disabled')
        assert submit_page.public_data_input.absent()
        submit_page.public_available_button.click()
        assert submit_page.public_data_input.present()
        submit_page.public_data_input.click()
        submit_page.public_data_input.send_keys_deliberately('https://osf.io/')
        # Need to scroll down since the Preregistration radio buttons are obscured by the Dev mode warning in test environments
        currentYPos = driver.execute_script('return window.scrollY;')
        driver.execute_script('window.scrollTo(0, arguments[0])', currentYPos + 200)
        assert submit_page.preregistration_input.absent()
        submit_page.preregistration_no_button.click()
        assert submit_page.preregistration_input.present()
        submit_page.preregistration_input.click()
        submit_page.preregistration_input.send_keys_deliberately('QA Testing')
        # Save button is now enabled so we can use the object as defined in pages/preprints.py
        assert submit_page.save_author_assertions.is_enabled()
        submit_page.save_author_assertions.click()

        submit_page.basics_license_dropdown.click()
        # The order of the options in the license dropdown is not consistent across test environments, so we can't use the
        # basics_universal_license element as defined in pages/preprints.py since it uses its index position (3rd option in list)
        licenseSelect = Select(submit_page.basics_license_dropdown)
        licenseSelect.select_by_visible_text('CC0 1.0 Universal')
        # Need to scroll down since the Keyword/tags section is obscured by the Dev mode warning in the test environments
        currentYPos = driver.execute_script('return window.scrollY;')
        driver.execute_script('window.scrollTo(0, arguments[0])', currentYPos + 200)
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

        # Conflict of Interest section:
        assert driver.find_element(By.CSS_SELECTOR, '[data-test-coi-continue]').get_property('disabled')
        assert submit_page.no_coi_text_box.absent()
        submit_page.conflict_of_interest_no.click()
        assert submit_page.no_coi_text_box.present()
        assert submit_page.coi_save_button.is_enabled()
        submit_page.coi_save_button.click()

        # Wait for Supplemental materials to show
        submit_page.supplemental_create_new_project.click()
        submit_page.supplemental_save_button.click()

        submit_page.create_preprint_button.click()
        submit_page.modal_create_preprint_button.click()

        preprint_detail = PreprintDetailPage(driver, verify=True)
        WebDriverWait(driver, 10).until(EC.visibility_of(preprint_detail.title))

        assert preprint_detail.title.text == preprint_project.title
        # All 3 Author Assertion sections on Detail page are not displaying in Stage 1 for some reason
        if not settings.STAGE1:
            assert preprint_detail.coi_assert_container.text == 'Conflict of InterestNo'
            preprint_detail.coi_dropdown_arrow.click()
            assert preprint_detail.dropdown_content.text == 'Author asserted no Conflict of Interest'
            assert preprint_detail.pub_data_assert_container.text == 'Public DataAvailable'
            preprint_detail.pub_data_dropdown_arrow.click()
            assert preprint_detail.dropdown_content.text == 'https://osf.io/'
            assert preprint_detail.prereg_assert_container.text == 'PreregistrationNo'
            preprint_detail.prereg_dropdown_arrow.click()
            assert preprint_detail.dropdown_content.text == 'QA Testing'
        assert preprint_detail.abstract_text.text == 'Center for Open Selenium'
        assert preprint_detail.license_text.text == 'License\nCC0 1.0 Universal'
        preprint_detail.license_detail_arrow.click()
        assert 'Statement of Purpose' in preprint_detail.license_detail_text.text
        assert preprint_detail.discipline_text.text == 'Architecture'
        assert preprint_detail.fileName.text == 'osf selenium test file for testing because its fake.txt'

        match = re.search(r'Supplemental Materials\s+([a-z0-9]{4,8})\.osf\.io/([a-z0-9]{5})', preprint_detail.view_page.text)
        assert match is not None
        sleep(3)

        # Now go back to the OSF landing page and search for the preprint we just created and verify that it appears in search
        # results and that we can open the details page from there
        landing_page.goto()
        landing_page.search_input.click()
        landing_page.search_input.send_keys(preprint_project.title)
        landing_page.search_button.click()
        discover_page = PreprintDiscoverPage(driver, verify=True)
        discover_page.loading_indicator.here_then_gone()
        search_results = discover_page.search_results
        # It may take a few seconds for the newly created preprint to appear in the search results
        preprint_found = False
        count = 0
        while not preprint_found:
            count += 1
            if search_results[0].text == preprint_project.title:
                preprint_found = True
            else:
                discover_page.search_button.click()
                sleep(1)
                discover_page.loading_indicator.here_then_gone()
                # need to refresh the search results list
                search_results = driver.find_elements(By.CSS_SELECTOR, '.search-result h4 > a')
                if count > 5:
                    raise Exception('Could not find preprint in search results')
                    break

        search_results[0].click()
        preprint_detail = PreprintDetailPage(driver, verify=True)
        WebDriverWait(driver, 10).until(EC.visibility_of(preprint_detail.title))
        assert preprint_detail.title.text == preprint_project.title
        if not settings.STAGE1:
            assert preprint_detail.coi_assert_container.text == 'Conflict of InterestNo'
            preprint_detail.coi_dropdown_arrow.click()
            assert preprint_detail.dropdown_content.text == 'Author asserted no Conflict of Interest'
            assert preprint_detail.pub_data_assert_container.text == 'Public DataAvailable'
            preprint_detail.pub_data_dropdown_arrow.click()
            assert preprint_detail.dropdown_content.text == 'https://osf.io/'
            assert preprint_detail.prereg_assert_container.text == 'PreregistrationNo'
            preprint_detail.prereg_dropdown_arrow.click()
            assert preprint_detail.dropdown_content.text == 'QA Testing'
        assert preprint_detail.abstract_text.text == 'Center for Open Selenium'
        assert preprint_detail.license_text.text == 'License\nCC0 1.0 Universal'
        preprint_detail.license_detail_arrow.click()
        assert 'Statement of Purpose' in preprint_detail.license_detail_text.text
        assert preprint_detail.discipline_text.text == 'Architecture'
        assert preprint_detail.fileName.text == 'osf selenium test file for testing because its fake.txt'

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

    @pytest.fixture(params=providers(), ids=[prov['id'] for prov in providers()])
    def provider(self, request):
        return request.param

    def test_landing_page_loads(self, driver, provider):
        PreprintLandingPage(driver, provider=provider).goto()
        if provider['attributes']['domain_redirect_enabled']:
            # Make sure the landing page url matches the expected domian
            assert driver.current_url == provider['attributes']['domain']
        else:
            assert 'osf.io/preprints/' in driver.current_url

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


# The following class only runs in Production for Branded Providers that have a Custom Domain
@markers.smoke_test
@markers.core_functionality
@pytest.mark.skipif(not settings.PRODUCTION, reason='Cannot test on stagings as they share SHARE')
class TestCustomDomainsInProd:

    @pytest.fixture(params=custom_providers(), ids=[prov['id'] for prov in custom_providers()])
    def provider(self, request):
        return request.param

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
