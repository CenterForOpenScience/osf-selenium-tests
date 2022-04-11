import logging
import re
from datetime import datetime

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

import markers
import settings
from api import osf_api
from pages.preprints import (
    PreprintDetailPage,
    PreprintDiscoverPage,
    PreprintLandingPage,
    PreprintSubmitPage,
)
from utils import find_current_browser


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
    def test_create_preprint_from_landing(
        self, session, driver, landing_page, project_with_file
    ):
        supplemental_guid = None
        try:
            # Create a date and time stamp before starting the creation of the preprint.
            # This may be used later to find the guid for the preprint.
            now = datetime.utcnow()
            date_time_stamp = now.strftime('%Y-%m-%dT%H:%M:%S')

            landing_page.add_preprint_button.click()
            submit_page = PreprintSubmitPage(driver, verify=True)

            # Wait for select a service to show
            WebDriverWait(driver, 10).until(
                EC.visibility_of(submit_page.select_a_service_help_text)
            )
            submit_page.select_a_service_save_button.click()
            submit_page.upload_from_existing_project_button.click()
            submit_page.upload_project_selector.click()
            submit_page.upload_project_help_text.here_then_gone()
            submit_page.upload_project_selector_project.click()

            submit_page.upload_select_file.click()
            submit_page.upload_file_save_continue.click()

            # Author Assertions section
            # Note: We can't use the submit_page.save_author_assertions object here,
            # because it is disabled and any time we use an object defined in
            # pages/preprints.py it uses get_web_element() in the Locator class.
            # Within get_web_element() the element_to_be_clickable method is used,
            # and this method will always fail for disabled objects.  So in this
            # instance we have to get the button object using the driver.find_element
            # method while it is disabled.  After the button becomes enabled (i.e.
            # after required data has been provided) then we can use the
            # submit_page.save_author_assertions object to check the disabled
            # property.  See implementation below.
            assert driver.find_element(
                By.CSS_SELECTOR, '[data-test-author-assertions-continue]'
            ).get_property('disabled')
            assert submit_page.public_data_input.absent()
            submit_page.public_available_button.click()
            assert submit_page.public_data_input.present()
            submit_page.public_data_input.click()
            submit_page.public_data_input.send_keys_deliberately('https://osf.io/')
            # Need to scroll down since the Preregistration radio buttons are obscured
            # by the Dev mode warning in test environments
            submit_page.scroll_into_view(submit_page.preregistration_no_button.element)
            assert submit_page.preregistration_input.absent()
            submit_page.preregistration_no_button.click()
            assert submit_page.preregistration_input.present()
            submit_page.preregistration_input.click()
            submit_page.preregistration_input.send_keys_deliberately('QA Testing')
            # Save button is now enabled so we can use the object as defined in
            # pages/preprints.py
            assert submit_page.save_author_assertions.is_enabled()
            submit_page.save_author_assertions.click()

            submit_page.basics_license_dropdown.click()
            # The order of the options in the license dropdown is not consistent across
            # test environments. So we have to select by the actual text value instead
            # of by relative position (i.e. 3rd option in listbox).
            license_select = Select(submit_page.basics_license_dropdown)
            license_select.select_by_visible_text('CC0 1.0 Universal')
            # Need to scroll down since the Keyword/tags section is obscured by the Dev
            # mode warning in the test environments
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

            # Conflict of Interest section:
            assert driver.find_element(
                By.CSS_SELECTOR, '[data-test-coi-continue]'
            ).get_property('disabled')
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

            assert preprint_detail.title.text == project_with_file.title
            # Capture guid of supplemental materials project created during workflow
            match = re.search(
                r'Supplemental Materials\s+([a-z0-9]{4,8})\.osf\.io/([a-z0-9]{5})',
                preprint_detail.view_page.text,
            )
            assert match is not None
            supplemental_guid = match.group(2)

        finally:
            # If there was an error above and we did not capture the guid for the
            # supplemental materials project, then we need to get it if it exists.
            if supplemental_guid is None:
                # Get the list of preprints for the current user
                preprints = osf_api.get_preprints_list_for_user(session)
                for preprint in preprints:
                    # Go through the list of preprints and if any of them has a creation
                    # date and time after the date time stamp that we created before
                    # starting this preprint then that is our preprint, so use its guid
                    # to get the guid for the supplemental materials project.
                    if preprint['attributes']['date_created'] > date_time_stamp:
                        supplemental_guid = (
                            osf_api.get_preprint_supplemental_material_guid(
                                session, preprint['id']
                            )
                        )
                        break

            # We need to always delete the supplemental materials project if it exists
            if supplemental_guid is not None:
                osf_api.delete_project(session, supplemental_guid, None)

            # If we are still stuck on the Preprint Submit page then refresh it to see
            # if we get an alert pop-up message about leaving the page.  If so then
            # accept the alert so that we can get off this page and can proceed with
            # the rest of the tests.
            if submit_page.verify():
                submit_page.reload()
                try:
                    WebDriverWait(driver, 3).until(EC.alert_is_present())
                    driver.switch_to.alert.accept()
                except TimeoutException:
                    pass


class TestPreprintSearch:
    @markers.smoke_test
    @markers.core_functionality
    def test_search_results_exist(self, driver, landing_page):
        landing_page.search_button.click()
        discover_page = PreprintDiscoverPage(driver, verify=True)
        discover_page.loading_indicator.here_then_gone()
        assert len(discover_page.search_results) > 0

    def test_preprint_detail_page(self, driver):
        discover_page = PreprintDiscoverPage(driver)
        discover_page.goto()
        assert PreprintDiscoverPage(driver, verify=True)
        if not settings.PRODUCTION:
            # Since all of the testing environments use the same SHARE server, we need
            # to enter a value in the search input box that will ensure that the results
            # are specific to the current environment.  We can do this by searching for
            # the test environment url in the identifiers metadata field.
            environment_url = settings.OSF_HOME[
                8:
            ]  # Need to strip out "https://" from the url
            search_text = 'identifiers:"' + environment_url + '"'
            discover_page.search_box.send_keys_deliberately(search_text)
            discover_page.search_box.send_keys(Keys.ENTER)
            if settings.STAGE2:
                # Stage 2 has a lot of old preprint data that is still listed in search
                # results but does not actually have preprint detail pages so we need to
                # sort the results so that the newest preprints are listed first.
                discover_page.sort_button.click()
                discover_page.sort_option_newest_to_oldest.click()
        discover_page.loading_indicator.here_then_gone()
        search_results = discover_page.search_results
        assert search_results
        # Click on first entry in search results to open the Preprint Detail page
        search_results[0].click()
        assert PreprintDetailPage(driver, verify=True)


@markers.smoke_test
class TestPreprintMetrics:
    @pytest.fixture(scope='session')
    def latest_preprint_node(self):
        """Return the node id of the latest preprint submitted in the given environment"""
        return osf_api.get_most_recent_preprint_node_id()

    def test_preprint_views_count(self, driver, latest_preprint_node):
        """Test the Views Count functionality on the Preprint Detail page by getting
        the views count for a preprint using the api and comparing it to the views
        count value displayed on the page. Also verifying that the views count will
        be incremented if the page is reloaded (only in testing environments).
        """
        api_views_count = osf_api.get_preprint_views_count(node_id=latest_preprint_node)
        preprint_page = PreprintDetailPage(driver, guid=latest_preprint_node)
        preprint_page.goto()
        assert PreprintDetailPage(driver, verify=True)
        page_views_count = int(preprint_page.views_downloads_counts.text[7:9])
        assert api_views_count == page_views_count
        # Don't reload the page in Production since we don't want to artificially
        # inflate the metrics
        if not settings.PRODUCTION:
            # Verify that the views count from the api increases by 1 after we reload
            # the page.
            preprint_page.reload()
            assert (
                osf_api.get_preprint_views_count(node_id=latest_preprint_node)
                == api_views_count + 1
            )

    def test_preprint_downloads_count(self, driver, latest_preprint_node):
        """Test the Downloads Count functionality on the Preprint Detail page by
        getting the downloads count for a preprint using the api and comparing it to
        the downloads count value displayed on the page. Also verifying that the
        downloads count will be incremented when the downloads button on the page is
        clicked (only in testing environments).
        """
        api_downloads_count = osf_api.get_preprint_downloads_count(
            node_id=latest_preprint_node
        )
        preprint_page = PreprintDetailPage(driver, guid=latest_preprint_node)
        preprint_page.goto()
        assert PreprintDetailPage(driver, verify=True)
        page_downloads_count = int(
            preprint_page.views_downloads_counts.text.split('Downloads:')[1]
        )
        assert api_downloads_count == page_downloads_count
        # Don't download the Preprint in Production since we don't want to artificially
        # inflate the metrics
        if not settings.PRODUCTION:
            # Verify that the downloads count from the api increases by 1 after we
            # download the document.
            preprint_page.download_button.click()
            assert (
                osf_api.get_preprint_downloads_count(node_id=latest_preprint_node)
                == api_downloads_count + 1
            )


@pytest.fixture(scope='session')
def providers():
    """Return all preprint providers."""
    return osf_api.get_providers_list()


@pytest.fixture(scope='session')
def custom_providers():
    """Return the API data of all preprint providers with custom domains."""
    providers = osf_api.get_providers_list()
    return [
        provider
        for provider in providers
        if provider['attributes']['domain_redirect_enabled']
    ]


class TestProvidersWithCustomDomains:
    @pytest.fixture(
        params=custom_providers(), ids=[prov['id'] for prov in custom_providers()]
    )
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
@pytest.mark.skipif(
    not settings.PRODUCTION,
    reason='Most of the Branded Preprint Provider pages in test environments have no preprints',
)
class TestBrandedProviders:
    """This class only runs in Production for all Branded Providers"""

    @pytest.fixture(params=providers(), ids=[prov['id'] for prov in providers()])
    def provider(self, request):
        return request.param

    def test_detail_page(self, session, driver, provider):
        """Test a preprint detail page by grabbing the first search result from the discover page."""
        discover_page = PreprintDiscoverPage(driver, provider=provider)

        # This fails only in firefox because of selenium incompatibilities with right-left languages
        if 'firefox' in find_current_browser(driver) and 'arabixiv' in provider['id']:
            discover_page.url_addition += '?q=Analysis'

        # As of January 24, 2022, the Engineering Archive ('engrxiv') preprint provider
        # has switched away from using OSF as their preprint service.  Therefore the
        # web page that OSF automatically redirects to is no longer based on the OSF
        # Preprints landing/discover page design.  However, they remain in our active
        # preprint provider list in the OSF api due to legal issues that are still being
        # worked out.  The best guess is that the transition will be completed (and
        # engrxiv removed from the api list) by the end of the first quarter of 2022
        # (i.e. end of March).  So to prevent this test from failing in Production
        # every night for 'engrxiv' we are going to skip the following steps for this
        # provider.
        if 'engrxiv' not in provider['id']:
            discover_page.goto()
            discover_page.verify()
            # add OSF consent cookie to get rid of the banner at the bottom of the page which can get in the way
            # when we have to scroll down to click the first preprint listing
            driver.add_cookie({'name': 'osf_cookieconsent', 'value': '1'})
            discover_page.reload()
            discover_page.loading_indicator.here_then_gone()

            if osf_api.get_providers_total(provider['id'], session=session):
                search_results = discover_page.search_results
                assert search_results
                search_results[0].click()
                PreprintDetailPage(driver, verify=True)
            elif not provider['attributes']['additional_providers']:
                # Some Preprint Providers may also display preprints from other sources not
                # just OSF. So we do not want to assert that there are No Results when there
                # may be results from non-OSF providers.
                assert discover_page.no_results
