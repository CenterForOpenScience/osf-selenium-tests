import logging

import pytest
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import markers
import settings
import utils
from api import osf_api
from pages.project import (
    FilesMetadataPage,
    FilesPage,
    ProjectMetadataPage,
)
from pages.registries import RegistrationMetadataPage


logger = logging.getLogger(__name__)


@pytest.fixture()
def file_guid(driver, default_project, session, provider='osfstorage'):

    node_id = default_project.id
    node = osf_api.get_node(session, node_id=node_id)

    if settings.PREFERRED_NODE:
        new_file, metadata = osf_api.get_existing_file_data(session)
        files_page = FilesPage(
            driver, guid=settings.PREFERRED_NODE, addon_provider=provider
        )
        files_page.goto()
        # Wait for File List items to load
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-test-file-list-item]')
            )
        )
        row = utils.find_row_by_name(files_page, new_file)

        file_link = row.find_element_by_css_selector('[data-test-file-list-link]')
        file_link.click()
        driver.switch_to.window(driver.window_handles[0])
        file_id = metadata['data'][0]['attributes']['path']
        file_guid = osf_api.get_fake_file_guid(session, file_id)
        return file_guid

    else:
        try:
            new_file, metadata = osf_api.upload_fake_file(
                session=session,
                node=node,
                name='files_metadata_test.txt',
                provider=provider,
            )

            files_page = FilesPage(driver, guid=node_id, addon_provider=provider)
            files_page.goto()
            if '404' in driver.page_source:
                raise Exception
            else:
                # Wait for File List items to load
                WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, '[data-test-file-list-item]')
                    )
                )
                row = utils.find_row_by_name(files_page, new_file)

                file_link = row.find_element_by_css_selector(
                    '[data-test-file-list-link]'
                )
                file_link.click()
                driver.switch_to.window(driver.window_handles[0])
                file_id = metadata['data']['attributes']['path']
                file_guid = osf_api.get_fake_file_guid(session, file_id)
                return file_guid

        except Exception:
            logger.error('Server error occurred')
            osf_api.delete_addon_files(
                session, provider, current_browser=settings.DRIVER, guid=node_id
            )


@pytest.fixture()
def file_metadata_page(driver, session, file_guid):
    osf_api.update_file_metadata(session, file_guid)
    file_metadata_page = FilesMetadataPage(driver, guid=file_guid)
    file_metadata_page.goto()
    return file_metadata_page


def get_funder_information(funder_name):
    """This method is used to get the funder information for the
    given funder name using api link"""
    url = settings.FUNDER_INFO_URL
    response = requests.get(url)
    data = response.json()
    for funder in data['included']:
        if funder['type'] == 'index-card':
            if (
                funder['attributes']['resourceMetadata']['name'][0]['@value']
                == funder_name
            ):

                award_title = funder['attributes']['resourceMetadata']['resourceType'][
                    0
                ]['@id']
                award_uri = funder['attributes']['resourceIdentifier'][0]
                award_number = funder['id']

    return award_title, award_uri, award_number


@pytest.mark.usefixtures('must_be_logged_in')
@markers.smoke_test
@markers.core_functionality
class TestFilesMetadata:
    def test_change_file_metadata_title(self, driver, file_metadata_page, fake):
        """This test verifies that the file metadata field
        title is editable and changes are saved."""

        new_title = fake.sentence(nb_words=1)
        orig_title = file_metadata_page.files_metadata_title.text
        assert orig_title != new_title
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-test-edit-metadata-button]')
            )
        ).click()

        file_metadata_page.edit_title.click()
        title_input = driver.find_element_by_css_selector(
            '[data-test-title-field] textarea'
        )
        title_input.clear()
        title_input.send_keys(new_title)
        file_metadata_page.save_metadata_button.click()
        assert new_title == utils.clean_text(
            file_metadata_page.files_metadata_title.text
        )
        file_metadata_tab = utils.switch_to_new_tab(driver)
        utils.close_current_tab(driver, file_metadata_tab)

    def test_change_file_metadata_description(self, driver, file_metadata_page, fake):
        """This test verifies that the file metadata field
        description is editable and changes are saved."""

        new_description = fake.sentence(nb_words=1)
        orig_description = file_metadata_page.files_metadata_description.text
        assert orig_description != new_description

        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-test-edit-metadata-button]')
            )
        ).click()

        description_input = driver.find_element_by_css_selector(
            '[data-test-description-field] textarea'
        )
        description_input.clear()
        description_input.send_keys(new_description)
        file_metadata_page.save_metadata_button.click()
        assert new_description == utils.clean_text(
            file_metadata_page.files_metadata_description.text
        )
        file_metadata_tab = utils.switch_to_new_tab(driver)
        utils.close_current_tab(driver, file_metadata_tab)

    def test_change_file_metadata_resource_type(self, driver, file_metadata_page):
        """This test verifies that the file metadata field
        resource type is editable and changes are saved."""

        orig_resource_type = file_metadata_page.files_metadata_resource_type.text

        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-test-edit-metadata-button]')
            )
        ).click()
        # Select 'Collection' from the resource type listbox
        file_metadata_page.resource_type.click()
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    '#ember-basic-dropdown-wormhole > div > ul > li>span',
                )
            )
        )
        file_metadata_page.select_from_dropdown_listbox('Collection')

        file_metadata_page.save_metadata_button.click()
        assert (
            orig_resource_type != file_metadata_page.files_metadata_resource_type.text
        )
        file_metadata_tab = utils.switch_to_new_tab(driver)
        utils.close_current_tab(driver, file_metadata_tab)

    def test_change_file_metadata_resource_language(self, driver, file_metadata_page):
        """This test verifies that the file metadata field
        resource language is editable and changes are saved."""
        orig_resource_language = (
            file_metadata_page.files_metadata_resource_language.text
        )

        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-test-edit-metadata-button]')
            )
        ).click()
        # Select 'Bengali' from the resource language listbox
        file_metadata_page.resource_language.click()
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    '#ember-basic-dropdown-wormhole > div > ul > li>span',
                )
            )
        )
        file_metadata_page.select_from_dropdown_listbox('Bengali')

        file_metadata_page.save_metadata_button.click()
        assert (
            orig_resource_language
            != file_metadata_page.files_metadata_resource_language.text
        )
        file_metadata_tab = utils.switch_to_new_tab(driver)
        utils.close_current_tab(driver, file_metadata_tab)

    def test_cancel_file_metadata_changes(self, driver, file_metadata_page, fake):
        """This test verifies the file metadata fields
        title, Description, Resource Type and Resource Language are editable
        and changes are cancelled without saving.
        """
        new_title = fake.sentence(nb_words=1)
        orig_title = file_metadata_page.files_metadata_title.text
        assert orig_title != new_title
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-test-edit-metadata-button]')
            )
        ).click()

        file_metadata_page.edit_title.click()
        title_input = driver.find_element_by_css_selector(
            '[data-test-title-field] textarea'
        )
        title_input.clear()
        title_input.send_keys(new_title)
        file_metadata_page.cancel_editing_button.click()
        assert new_title != file_metadata_page.files_metadata_title.text
        file_metadata_tab = utils.switch_to_new_tab(driver)
        utils.close_current_tab(driver, file_metadata_tab)

    @pytest.mark.skipif(
        settings.env('TEST_BUILD') == 'edge',
        reason='Test fails on remote edge browser because of download popup window',
    )
    def test_download_file_metadata(self, driver, file_metadata_page):
        """This test verifies download functionality for file metadata."""

        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '[data-test-download-button]')
                )
            ).click()

            if '404' in driver.page_source:
                raise Exception
            else:
                file_metadata_page.reload()
                FilesMetadataPage(driver, verify=True)

                # Verify File Download Functionality
                if settings.DRIVER != 'Remote':
                    url = driver.find_element_by_css_selector(
                        '[data-test-download-button]'
                    ).get_attribute('href')
                    guid = utils.get_guid_from_url(url, 3)
                    filename = utils.latest_download_file()
                    assert guid in filename
                else:
                    utils.verify_file_download(driver, file_name='')

        except Exception:
            logger.error('404 Exception caught')
        file_metadata_tab = utils.switch_to_new_tab(driver)
        utils.close_current_tab(driver, file_metadata_tab)


@pytest.mark.usefixtures('must_be_logged_in')
@markers.smoke_test
@markers.core_functionality
class TestProjectMetadata:
    @pytest.fixture()
    def project_metadata_page(self, driver, default_project_with_metadata):
        project_metadata_page = ProjectMetadataPage(
            driver, guid=default_project_with_metadata.id
        )
        project_metadata_page.goto()
        return project_metadata_page

    def test_edit_metadata_description(self, driver, project_metadata_page, fake):
        """This test verifies that the node level metadata field
        description is editable and changes are saved."""

        new_description = fake.sentence(nb_words=4)

        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-test-edit-node-description-button]')
            )
        ).click()

        description_input = driver.find_element_by_css_selector(
            '[data-test-description-field] textarea'
        )
        description_input.clear()
        description_input.send_keys(new_description)
        project_metadata_page.save_description_button.click()
        assert new_description == utils.clean_text(
            project_metadata_page.description.text
        )

    def test_edit_contributors(
        self, session, driver, project_metadata_page, default_project_with_metadata
    ):
        """This test verifies that user can add/remove
        contributors to project metadata."""

        if settings.DOMAIN == 'test':
            new_user = 'Selenium Test User (Do Not Use)'
        elif settings.DOMAIN == 'prod':
            new_user = 'OSF Tester1'
        else:
            new_user = 'Selenium Staging'

        # Delete the user if its already exists
        osf_api.delete_project_contributor(
            session, node_id=default_project_with_metadata.id, user_name=new_user
        )
        project_metadata_page.goto_with_reload()

        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-test-edit-contributors]')
            )
        ).click()

        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    'a.btn.btn-success.btn-sm.m-l-md[href="#addContributors"]',
                )
            )
        ).click()

        project_metadata_page.search_input.click()
        project_metadata_page.search_input.send_keys(new_user)
        project_metadata_page.contributor_search_button.click()

        # Get the row number for the user from the search table
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    '//div[@class="row"]/div[@class="col-md-4"]/table[@class="table-condensed table-hover"]',
                )
            )
        )
        search_table_path = '//table[@class="table-condensed table-hover"]'
        rno, search_table_data = utils.read_data_from_table(
            driver, search_table_path, check_match=True, item_match=new_user
        )
        # Click on the Add button of the row number for the user from the search table to add the new contributor user
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, search_table_path + '/tbody/tr[' + str(rno) + ']/td[1]')
            )
        ).click()

        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@class="btn btn-success"]'))
        ).click()

        project_metadata_page.reload()
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//table[@id="manageContributorsTable"]')
            )
        )
        contributor_table_path = '//table[@id="manageContributorsTable"]'
        # Get the total number of rows in contributors table
        rowno, contributor_table_data = utils.read_data_from_table(
            driver, contributor_table_path, check_match=False
        )

        # Get the user name from the last row which is added recently
        user = driver.find_element_by_xpath(
            contributor_table_path + '/tbody/tr[' + str(rowno) + ']/td[2]'
        )
        assert new_user in user.text

    def test_edit_resource_information(self, driver, project_metadata_page):
        """This test verifies that user can add/remove
        resource information to project metadata."""
        orig_resource_type = project_metadata_page.resource_type.text
        orig_resource_language = project_metadata_page.resource_language.text

        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-test-edit-resource-metadata-button]')
            )
        ).click()

        # Select 'Book' from the resource type listbox
        project_metadata_page.resource_type_dropdown.click()
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    '#ember-basic-dropdown-wormhole > div > ul > li>span',
                )
            )
        )
        project_metadata_page.select_from_dropdown_listbox('Book')
        # Select 'Bengali' from the resource language listbox
        project_metadata_page.resource_language_dropdown.click()
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    '#ember-basic-dropdown-wormhole > div > ul > li>span',
                )
            )
        )
        project_metadata_page.select_from_dropdown_listbox('Bengali')

        project_metadata_page.resource_information_save_button.click()
        assert orig_resource_type != project_metadata_page.resource_type.text
        assert orig_resource_language != project_metadata_page.resource_language.text

    def test_edit_support_funding_information(
        self, session, driver, project_metadata_page, default_project_with_metadata
    ):
        """This test verifies that user can add/remove
        funder information to project metadata."""

        funder_name = 'NFL Charities'
        # Get the funder information for the given funder name
        award_title, award_uri, award_number = get_funder_information(funder_name)
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-test-edit-funding-metadata-button]')
            )
        ).click()
        # Delete funder info if already exists
        funder_info = osf_api.get_funder_data_project(
            session, project_guid=default_project_with_metadata.id
        )
        if funder_info is not None:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//button[text()="Delete funder"]')
                )
            ).click()

        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Add funder"]'))
        ).click()

        project_metadata_page.funder_name.click()

        project_metadata_page.funder_name_search_input.send_keys(funder_name)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-option-index="0"]')
            )
        ).click()
        project_metadata_page.award_title.click()
        project_metadata_page.award_title.send_keys(award_title)
        project_metadata_page.award_info_URI.click()
        project_metadata_page.award_info_URI.send_keys(award_uri)
        project_metadata_page.award_number.click()
        project_metadata_page.award_number.send_keys(award_number)
        project_metadata_page.add_funder_button.click()
        project_metadata_page.scroll_into_view(
            project_metadata_page.delete_funder_button.element
        )

        project_metadata_page.delete_funder_button.click()
        project_metadata_page.save_funder_info_button.click()

        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-test-metadata-header]')
            )
        )

        assert funder_name in project_metadata_page.display_funder_name.text
        assert award_title in project_metadata_page.display_award_title.text
        assert award_number in project_metadata_page.display_award_number.text
        assert award_uri in project_metadata_page.dispaly_award_info_uri.text


@pytest.mark.usefixtures('must_be_logged_in_as_registration_user')
@markers.dont_run_on_prod
@markers.core_functionality
class TestRegistrationMetadata:
    @pytest.fixture()
    def registration_metadata_page(self, driver):
        registration_guid = osf_api.get_registration_by_title(
            'Selenium Registration for Metadata tests'
        )
        osf_api.update_registration_metadata_with_custom_data(registration_guid)
        registration_metadata_page = RegistrationMetadataPage(
            driver, guid=registration_guid
        )
        registration_metadata_page.goto()
        return registration_metadata_page

    def test_edit_metadata_description(self, driver, registration_metadata_page, fake):
        """This test verifies that the registration metadata field
        description is editable and changes are saved."""

        new_description = fake.sentence(nb_words=4)

        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-test-edit-node-description-button]')
            )
        ).click()

        description_input = driver.find_element_by_css_selector(
            '[data-test-description-field] textarea'
        )
        description_input.clear()
        description_input.send_keys(new_description)
        registration_metadata_page.save_metadata_description_button.click()
        assert new_description == utils.clean_text(
            registration_metadata_page.metadata_description.text
        )

    def test_edit_resource_information(self, driver, registration_metadata_page):
        """This test verifies that user can add/remove
        resource information to registration metadata."""

        orig_resource_type = registration_metadata_page.resource_type.text
        orig_resource_language = registration_metadata_page.resource_language.text

        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-test-edit-resource-metadata-button]')
            )
        ).click()

        # Select 'Book' from the resource type listbox
        registration_metadata_page.resource_type_dropdown.click()
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    '#ember-basic-dropdown-wormhole > div > ul > li>span',
                )
            )
        )
        registration_metadata_page.select_from_dropdown_listbox('Book')
        # Select 'Bengali' from the resource language listbox
        registration_metadata_page.resource_language_dropdown.click()
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    '#ember-basic-dropdown-wormhole > div > ul > li>span',
                )
            )
        )
        registration_metadata_page.select_from_dropdown_listbox('Bengali')

        registration_metadata_page.resource_information_save_button.click()
        assert orig_resource_type != utils.clean_text(
            registration_metadata_page.resource_type.text
        )
        assert orig_resource_language != utils.clean_text(
            registration_metadata_page.resource_language.text
        )

    def test_edit_support_funding_information(
        self, driver, registration_metadata_page, session
    ):
        """This test verifies that user can add/remove
        funder information to registration metadata."""

        funder_name = 'NFL Charities'
        # Get funder information for the given funder name
        award_title, award_info_uri, award_number = get_funder_information(funder_name)

        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-test-edit-funding-metadata-button]')
            )
        ).click()
        registration_guid = osf_api.get_registration_by_title(
            'Selenium Registration for Metadata tests'
        )
        funder_info = osf_api.get_funder_data_registration(registration_guid)
        if funder_info is not None:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//button[text()="Delete funder"]')
                )
            ).click()

        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Add funder"]'))
        ).click()

        registration_metadata_page.funder_name.click()

        registration_metadata_page.funder_name_search_input.send_keys(funder_name)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-option-index="0"]')
            )
        ).click()
        registration_metadata_page.award_title.click()
        registration_metadata_page.award_title.send_keys(award_title)
        registration_metadata_page.award_info_URI.click()
        registration_metadata_page.award_info_URI.send_keys(award_info_uri)
        registration_metadata_page.award_number.click()
        registration_metadata_page.award_number.send_keys(award_number)
        registration_metadata_page.add_funder_button.click()

        registration_metadata_page.scroll_into_view(
            registration_metadata_page.delete_funder_button.element
        )

        registration_metadata_page.delete_funder_button.click()

        registration_metadata_page.save_funder_info_button.click()
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-test-metadata-header]')
            )
        )

        assert funder_name in registration_metadata_page.display_funder_name.text
        assert award_title in registration_metadata_page.display_award_title.text
        assert award_number in registration_metadata_page.display_award_number.text
        assert award_info_uri in registration_metadata_page.dispaly_award_info_uri.text
