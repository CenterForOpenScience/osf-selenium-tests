import pytest
from pythosf import client
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import markers
import settings
from api import osf_api
from pages.login import safe_login
from pages.registries import (
    DraftRegistrationAnalysisPlanPage,
    DraftRegistrationDesignPlanPage,
    DraftRegistrationMetadataPage,
    DraftRegistrationOtherPage,
    DraftRegistrationReviewPage,
    DraftRegistrationSamplingPlanPage,
    DraftRegistrationStudyInfoPage,
    DraftRegistrationVariablesPage,
    RegistrationAddNewPage,
    RegistrationDetailPage,
    RegistrationTombstonePage,
    RegistriesDiscoverPage,
    RegistriesLandingPage,
)


@pytest.fixture
def landing_page(driver):
    landing_page = RegistriesLandingPage(driver)
    landing_page.goto()
    return landing_page


class TestRegistriesDiscoverPage:
    @markers.smoke_test
    @markers.core_functionality
    def test_search_results_exist(self, driver, landing_page):
        landing_page.search_box.send_keys_deliberately('QA Test')
        landing_page.search_box.send_keys(Keys.ENTER)
        discover_page = RegistriesDiscoverPage(driver, verify=True)
        discover_page.loading_indicator.here_then_gone()
        assert len(discover_page.search_results) > 0

    @markers.smoke_test
    @markers.core_functionality
    def test_detail_page(self, driver):
        """Test a registration detail page by grabbing the first search result from the discover page."""
        discover_page = RegistriesDiscoverPage(driver)
        discover_page.goto()
        if not settings.PRODUCTION:
            # Since all of the testing environments use the same SHARE server, we need to enter a value in the search
            # input box that will ensure that the results are specific to the current environment.  We can do this by
            # searching for the test environment in the affiliations metadata field.  The affiliated institutions as
            # setup in the testing environments typically include the specific environment in their names.
            # EX: The Center For Open Science [Stage2]
            if settings.STAGE1:
                # need to drop the 1 since they usually just use 'Stage' instead of 'Stage1'
                environment = 'stage'
            else:
                environment = settings.DOMAIN
            search_text = 'affiliations:' + environment
            discover_page.search_box.send_keys_deliberately(search_text)
            discover_page.search_box.send_keys(Keys.ENTER)
        discover_page.loading_indicator.here_then_gone()
        search_results = discover_page.search_results
        assert search_results

        target_registration = discover_page.get_first_non_withdrawn_registration()
        target_registration_title = target_registration.text
        target_registration.click()
        detail_page = RegistrationDetailPage(driver)
        detail_page.identity.present()
        assert RegistrationDetailPage(driver, verify=True)
        assert detail_page.identity.text in target_registration_title


@markers.smoke_test
@markers.core_functionality
class TestBrandedRegistriesPages:
    def providers():
        """Return all registration providers."""
        return osf_api.get_providers_list(type='registrations')

    @pytest.fixture(params=providers(), ids=[prov['id'] for prov in providers()])
    def provider(self, request):
        return request.param

    def test_discover_page(self, session, driver, provider):
        """This test will load the Discover page for each Branded Registry Provider that
        exists in an environment.
        """
        if provider['attributes']['branded_discovery_page']:
            discover_page = RegistriesDiscoverPage(driver, provider=provider)
            discover_page.goto()
            discover_page.loading_indicator.here_then_gone()
            assert RegistriesDiscoverPage(driver, verify=True)


@pytest.fixture
def login_as_user_with_registrations(driver):
    """Logs into OSF as the specific user for creating registrations."""
    safe_login(
        driver,
        user=settings.REGISTRATIONS_USER,
        password=settings.REGISTRATIONS_USER_PASSWORD,
    )


@markers.dont_run_on_prod
class TestRegistrationSubmission:
    @pytest.fixture
    def project_with_file_reg(self):
        """Returns a project with a file using the login session of the Registrations
        User.
        """
        session = client.Session(
            api_base_url=settings.API_DOMAIN,
            auth=(settings.REGISTRATIONS_USER, settings.REGISTRATIONS_USER_PASSWORD),
        )
        project = osf_api.create_project(session, title='OSF Registration Project')
        osf_api.upload_fake_file(
            session, project, name='osf selenium test file for registration.txt'
        )
        yield project
        project.delete()

    @pytest.fixture
    def add_new_page(self, driver, login_as_user_with_registrations):
        """Navigate to the Add New Registration page"""
        add_new_page = RegistrationAddNewPage(driver)
        add_new_page.goto()
        assert RegistrationAddNewPage(driver, verify=True)
        return add_new_page

    def test_submit_registration_from_project(
        self, driver, project_with_file_reg, add_new_page
    ):
        """This test creates a new draft registration from a project with a file
        attached starting from the Add New Registration page.  The test uses the OSF
        Preregistration schema template and enters data in all of the required template
        fields while leaving most of the other data fields empty. The completed draft
        registration is submitted and made public immediately (not embargoed). The
        associated project is then deleted as cleanup. The registration is permanent
        and cannot be deleted.
        """

        # Click the Yes has project radio button and verify that the Project listbox is
        # then displayed
        add_new_page.has_project_button.click()
        assert add_new_page.project_listbox_trigger.present()

        # Select the dummy project name from the listbox
        add_new_page.project_listbox_trigger.click()
        WebDriverWait(driver, 5).until(
            EC.text_to_be_present_in_element(
                (
                    By.CSS_SELECTOR,
                    '#ember-basic-dropdown-wormhole > div > ul >li.ember-power-select-option',
                ),
                'OSF Registration Project',
            )
        )
        add_new_page.select_from_dropdown_listbox('OSF Registration Project')

        # Select 'Open-Ended Registration' from the Schema listbox
        add_new_page.scroll_into_view(add_new_page.schema_listbox_trigger.element)
        add_new_page.schema_listbox_trigger.click()
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    '#ember-basic-dropdown-wormhole > div > ul >li.ember-power-select-option',
                )
            )
        )
        add_new_page.select_from_dropdown_listbox('OSF Preregistration')

        # Click the Create draft button and verify that we are navigated to the Draft
        # Registration Metadata page
        add_new_page.scroll_into_view(add_new_page.create_draft_button.element)
        add_new_page.create_draft_button.click()
        metadata_page = DraftRegistrationMetadataPage(driver, verify=True)

        # Enter data in the input fields on the Draft Metadata page
        metadata_page.title_input.clear()
        metadata_page.title_input.send_keys_deliberately(
            'Selenium Test Project With File Registration'
        )

        metadata_page.description_textarea.click()
        metadata_page.description_textarea.send_keys_deliberately(
            'This is a test registration created from a project using Selenium.'
        )

        metadata_page.scroll_into_view(metadata_page.category_listbox_trigger.element)
        metadata_page.category_listbox_trigger.click()
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    '#ember-basic-dropdown-wormhole > div > ul >li.ember-power-select-option',
                )
            )
        )
        metadata_page.select_from_dropdown_listbox('Software')
        metadata_page.scroll_into_view(metadata_page.license_listbox_trigger.element)
        metadata_page.license_listbox_trigger.click()
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    '#ember-basic-dropdown-wormhole > div > ul >li.ember-power-select-option',
                )
            )
        )
        metadata_page.select_from_dropdown_listbox('CC0 1.0 Universal')

        metadata_page.scroll_into_view(metadata_page.tags_input_box.element)
        metadata_page.select_top_level_subject('Engineering')
        WebDriverWait(driver, 5).until(
            EC.visibility_of(metadata_page.first_selected_subject)
        )
        assert metadata_page.first_selected_subject.text == 'Engineering'

        metadata_page.tags_input_box.click()
        metadata_page.tags_input_box.send_keys('selenium\r')

        metadata_page.scroll_into_view(metadata_page.next_page_button.element)
        metadata_page.next_page_button.click()

        # NOTE: On the following draft pages we are only going to enter data in the
        # required fields.

        # Study Information Page
        study_page = DraftRegistrationStudyInfoPage(driver, verify=True)
        assert study_page.page_heading.text == 'Study Information'

        study_page.hypothesis_textbox.click()
        study_page.hypothesis_textbox.send_keys_deliberately(
            'Hypothesis textbox - regression testing using selenium.'
        )

        study_page.next_page_button.click()

        # Design Plan Page
        design_page = DraftRegistrationDesignPlanPage(driver, verify=True)
        assert design_page.page_heading.text == 'Design Plan'

        design_page.other_radio_button.click()
        design_page.scroll_into_view(
            design_page.personnel_who_interact_checkbox.element
        )
        design_page.no_blinding_checkbox.click()
        design_page.scroll_into_view(design_page.study_design_textbox.element)
        design_page.study_design_textbox.click()
        design_page.study_design_textbox.send_keys_deliberately(
            'Study Design textbox - regression testing using selenium.'
        )

        # Verify file is attached
        design_page.scroll_into_view(design_page.first_file_name.element)
        assert (
            design_page.first_file_name.text
            == 'osf selenium test file for registration.txt'
        )

        design_page.scroll_into_view(design_page.next_page_button.element)
        design_page.next_page_button.click()

        # Sampling Plan Page
        sampling_page = DraftRegistrationSamplingPlanPage(driver, verify=True)
        assert sampling_page.page_heading.text == 'Sampling Plan'

        sampling_page.reg_following_radio_button.click()
        sampling_page.scroll_into_view(sampling_page.data_procedures_textbox.element)
        sampling_page.data_procedures_textbox.click()
        sampling_page.data_procedures_textbox.send_keys_deliberately(
            'Data Collection Procedures textbox - regression testing using selenium.'
        )
        sampling_page.scroll_into_view(sampling_page.first_file_name.element)
        assert (
            sampling_page.first_file_name.text
            == 'osf selenium test file for registration.txt'
        )

        # Purposely leave Sample Size textbox empty even though it is required

        sampling_page.scroll_into_view(sampling_page.next_page_button.element)
        sampling_page.next_page_button.click()

        # Variables Page
        variables_page = DraftRegistrationVariablesPage(driver, verify=True)
        assert variables_page.page_heading.text == 'Variables'

        # Verify that the Required Data Missing Indicator now displays in the left
        # sidebar since we left a required textbox empty on the previous page.
        variables_page.missing_data_ind.present()

        # Verify file is attached
        variables_page.scroll_into_view(variables_page.first_file_name.element)
        assert (
            variables_page.first_file_name.text
            == 'osf selenium test file for registration.txt'
        )

        variables_page.scroll_into_view(variables_page.measured_vars_textbox.element)
        variables_page.measured_vars_textbox.click()
        variables_page.measured_vars_textbox.send_keys_deliberately(
            'Measured Variables textbox - regression testing using selenium.'
        )

        variables_page.scroll_into_view(variables_page.next_page_button.element)
        variables_page.next_page_button.click()

        # Analysis Plan Page
        analysis_page = DraftRegistrationAnalysisPlanPage(driver, verify=True)
        assert analysis_page.page_heading.text == 'Analysis Plan'

        analysis_page.stat_models_textbox.click()
        analysis_page.stat_models_textbox.send_keys_deliberately(
            'Statistical Models textbox - regression testing using selenium.'
        )

        # Verify file is attached
        analysis_page.scroll_into_view(analysis_page.first_file_name.element)
        assert (
            analysis_page.first_file_name.text
            == 'osf selenium test file for registration.txt'
        )

        analysis_page.scroll_into_view(analysis_page.next_page_button.element)
        analysis_page.next_page_button.click()

        # Other Page
        other_page = DraftRegistrationOtherPage(driver, verify=True)
        assert other_page.page_heading.text == 'Other'

        other_page.other_textbox.click()
        other_page.other_textbox.send_keys_deliberately(
            'Other textbox - regression testing using selenium.'
        )

        other_page.review_page_button.click()

        # Review Page
        review_page = DraftRegistrationReviewPage(driver, verify=True)

        assert review_page.title.text == 'Selenium Test Project With File Registration'
        assert (
            review_page.description.text
            == 'This is a test registration created from a project using Selenium.'
        )
        assert review_page.category.text == 'Software'
        assert review_page.license.text == 'CC0 1.0 Universal'
        assert review_page.subject.text == 'Engineering'
        assert (
            review_page.tags.text
            == 'qatest selenium tests/test_registries.py::TestRegistrationSubmission::()::test_submit_registration_from_project (setup)'
        )

        # Verify the validation error since we intentionally left the required Sample
        # Size textbox empty
        assert (
            review_page.invalid_responses_text.text
            == 'Please address invalid or missing entries to complete registration.'
        )
        assert (
            review_page.sample_size_question_error.text == "This field can't be blank."
        )
        # Verify Register button is disabled
        assert driver.find_element(
            By.CSS_SELECTOR, 'button[data-test-goto-register]'
        ).get_attribute('disabled')

        # Go back to Sampling Plan page and enter data in Sample Size textbox
        review_page.sampling_plan_page_link.click()
        sampling_page = DraftRegistrationSamplingPlanPage(driver, verify=True)
        assert sampling_page.page_heading.text == 'Sampling Plan'
        sampling_page.scroll_into_view(sampling_page.sample_size_textbox.element)
        sampling_page.sample_size_textbox.click()
        sampling_page.sample_size_textbox.send_keys_deliberately(
            'Sample Size textbox - regression testing using selenium.'
        )
        # Click Next page button - need to force auto-save
        sampling_page.scroll_into_view(sampling_page.next_page_button.element)
        sampling_page.next_page_button.click()

        # Go back to Review Page and verify validation error has been cleared
        sampling_page.review_page_link.click()
        review_page = DraftRegistrationReviewPage(driver, verify=True)
        review_page.loading_indicator.here_then_gone()

        review_page.scroll_into_view(review_page.sample_size_response.element)
        assert review_page.invalid_responses_text.absent()
        assert review_page.sample_size_question_error.absent()
        assert (
            review_page.sample_size_response.text
            == 'Sample Size textbox - regression testing using selenium.'
        )

        review_page.scroll_into_view(review_page.register_button.element)
        review_page.register_button.click()
        # On modal - click radio button to make registration public immediately
        review_page.immediate_radio_button.click()
        review_page.submit_button.click()

        # Should get redirected to am Archiving Page with Registration in Pending
        # Admin Approval status
        tombstone_page = RegistrationTombstonePage(driver, verify=True)
        assert (
            tombstone_page.tombstone_title.text
            == 'This registration is currently archiving, and no changes can be made at this time.'
        )

        # NOTE: The archiving process can take a few minutes, after which an email is
        # sent to the user with a link to approve the registration. Since it can take up
        # to 5 minutes to receive this email it is not feasible to wait for this email
        # and approve the registration. Therefore we will allow the automatic approval
        # process to approve each registration which in the testing environments
        # typically occurs within a few hours.
