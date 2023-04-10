from datetime import datetime

from selenium.webdriver.common.by import By

import settings
from api import osf_api
from base.locators import (
    ComponentLocator,
    GroupLocator,
    Locator,
)
from components.dashboard import (
    CreateCollectionModal,
    CreateProjectModal,
    DeleteCollectionModal,
    ProjectCreatedModal,
)
from components.project import (
    ComponentCreatedModal,
    ComponentsPrivacyChangeModal,
    ConfirmDeleteDraftRegistrationModal,
    ConfirmFileDeleteModal,
    ConfirmPrivacyChangeModal,
    CreateComponentModal,
    CreateRegistrationModal,
    DeleteComponentModal,
    FileWidget,
    LogWidget,
    MoveCopyFileModal,
    RenameFileModal,
)
from pages.base import (
    GuidBasePage,
    OSFBasePage,
)


class ProjectPage(GuidBasePage):

    identity = Locator(By.ID, 'projectScope')
    title = Locator(By.ID, 'nodeTitleEditable', settings.LONG_TIMEOUT)
    title_input = Locator(By.CSS_SELECTOR, '.form-inline input')
    title_edit_submit_button = Locator(By.CSS_SELECTOR, '.editable-submit')
    title_edit_cancel_button = Locator(By.CSS_SELECTOR, '.editable-cancel')
    alert_message = Locator(By.CSS_SELECTOR, '#alert-container > p')
    parent_project_link = Locator(By.CSS_SELECTOR, 'h2.node-parent-title > a')
    description = Locator(By.ID, 'nodeDescriptionEditable')
    make_public_link = Locator(By.LINK_TEXT, 'Make Public')
    make_private_link = Locator(By.LINK_TEXT, 'Make Private')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-pulse')
    add_component_button = Locator(
        By.CSS_SELECTOR, '#newComponent > span > div.btn.btn-sm.btn-default'
    )
    collections_container = Locator(
        By.CSS_SELECTOR, '#projectBanner > div.row > div.collections-container.col-12'
    )
    pending_collection_display = Locator(
        By.CSS_SELECTOR,
        '#collections-header > div.pull-left > div',
    )
    collection_justification_link = Locator(By.CSS_SELECTOR, 'a.comment-popover')
    collection_justification_reason = Locator(By.CSS_SELECTOR, 'div.popover-content')
    first_collection_label = Locator(
        By.CSS_SELECTOR, '#collectionList > div > div:nth-child(3)'
    )
    first_collection_edit_link = Locator(By.CSS_SELECTOR, '#collectionList > div > a')
    first_collection_cancel_link = Locator(
        By.CSS_SELECTOR, 'a.fa.fa-close.collections-cancel-icon'
    )

    components = GroupLocator(By.ID, 'render-node')

    # Components
    file_widget = ComponentLocator(FileWidget)
    log_widget = ComponentLocator(LogWidget)
    confirm_privacy_change_modal = ComponentLocator(ConfirmPrivacyChangeModal)
    components_privacy_change_modal = ComponentLocator(ComponentsPrivacyChangeModal)
    create_component_modal = ComponentLocator(CreateComponentModal)
    component_created_modal = ComponentLocator(ComponentCreatedModal)
    delete_component_modal = ComponentLocator(DeleteComponentModal)

    def get_component_by_node_id(self, node_id):
        for component in self.components:
            if node_id == component.find_element_by_css_selector('div').get_attribute(
                'node_id'
            ):
                return component


def verify_log_entry(session, driver, node_id, action, **kwargs):
    """Helper function that verifies the most recent log entry in the log widget on a
    given project node. The log entry in the OSF api is also verified.
    """

    # Navigate to the Project Overview page
    project_page = ProjectPage(driver, guid=node_id)
    project_page.goto()
    project_page.loading_indicator.here_then_gone()
    project_title = project_page.title.text

    # Scroll down to the Log Widget and get the text from the first log entry
    project_page.scroll_into_view(project_page.log_widget.log_feed.element)
    log_item_1_text = project_page.log_widget.log_items[0].text

    # Get log entries for the project from the api
    logs = osf_api.get_node_logs(session, node_id=node_id)

    if action == 'osfstorage_file_removed':
        action = 'osf_storage_file_removed'

    # Look for the appropriate log entry and verify relevant details specific to the
    # log action type
    for entry in logs:
        if entry['attributes']['action'] == action:
            if 'file_removed' in action:
                # For File Deletion actions
                file_name = kwargs.get('file_name')
                provider = kwargs.get('provider')
                # Verify file name is in the path parameter attribute
                assert file_name in entry['attributes']['params']['path']
                # Verify that the first log item in the log widget describes the correct
                # file deletion action
                if provider == 'Owncloud':
                    log_text = 'removed file ' + file_name + ' from ownCloud'
                elif provider == 'Osfstorage':
                    log_text = 'removed file ' + file_name + ' from OSF Storage'
                elif provider == 'S3':
                    log_text = 'removed ' + file_name + ' in Amazon S3 bucket'
                else:
                    log_text = 'removed file ' + file_name + ' from ' + provider
            elif action == 'addon_file_moved':
                # For File Move actions
                file_name = kwargs.get('file_name')
                source = kwargs.get('source')
                if source == 'Owncloud':
                    source = 'ownCloud'
                elif source == 'S3':
                    source = 'Amazon S3'
                destination = kwargs.get('destination')
                # Verify move specific attributes in the api log entry
                assert (
                    entry['attributes']['params']['destination']['materialized']
                    == file_name
                )
                assert (
                    entry['attributes']['params']['destination']['addon'] == destination
                )
                assert (
                    entry['attributes']['params']['source']['materialized'] == file_name
                )
                assert entry['attributes']['params']['source']['addon'] == source
                # Verify that the first log item in the log widget describes the correct
                # file move action
                log_text = (
                    action[11:]
                    + ' '
                    + file_name
                    + ' in '
                    + source
                    + ' to '
                    + file_name
                    + ' in '
                    + destination
                )

            assert log_text in log_item_1_text
            break

    # The following data should be in all log entries:
    # Verify the log entry begins with the user name
    user = osf_api.current_user()
    assert log_item_1_text.startswith(user.full_name)
    assert entry['relationships']['user']['data']['id'] == user.id
    # Verify project title is in the log entry
    assert project_title in log_item_1_text
    assert entry['attributes']['params']['params_node']['title'] == project_title
    # Verify current date is also in the log entry
    now = datetime.now()
    date_today = now.strftime('%Y-%m-%d')
    assert date_today in log_item_1_text
    assert date_today in entry['attributes']['date']


class RequestAccessPage(GuidBasePage):

    identity = Locator(By.CSS_SELECTOR, '#requestAccessPrivateScope')


class MyProjectsPage(OSFBasePage):
    url = settings.OSF_HOME + '/myprojects/'

    identity = Locator(
        By.CSS_SELECTOR, '.col-xs-8 > h3:nth-child(1)', settings.LONG_TIMEOUT
    )
    create_project_button = Locator(By.CSS_SELECTOR, '[data-target="#addProject"]')
    create_collection_button = Locator(By.CSS_SELECTOR, '[data-target="#addColl"]')
    first_project = Locator(
        By.CSS_SELECTOR,
        'div[class="tb-tbody-inner"] > div:first-child > div:nth-child(1)',
    )
    first_project_hyperlink = Locator(
        By.CSS_SELECTOR,
        'div[data-rindex="0"] > div:first-child >' ' span:last-child > a:first-child',
    )
    first_custom_collection = Locator(By.CSS_SELECTOR, 'li[data-index="4"] span')
    first_collection_settings_button = Locator(
        By.CSS_SELECTOR, '.fa-ellipsis-v', settings.QUICK_TIMEOUT
    )
    first_collection_remove_button = Locator(
        By.CSS_SELECTOR, '[data-target="#removeColl"]', settings.QUICK_TIMEOUT
    )
    all_my_projects_and_components_link = Locator(
        By.CSS_SELECTOR, 'li[data-index="0"] span', settings.QUICK_TIMEOUT
    )
    empty_collection_indicator = Locator(By.CLASS_NAME, 'db-non-load-template')
    breadcrumbs = Locator(By.CSS_SELECTOR, 'div.db-breadcrumbs > ul > li > span')

    # Components
    create_collection_modal = ComponentLocator(CreateCollectionModal)
    delete_collection_modal = ComponentLocator(DeleteCollectionModal)
    create_project_modal = ComponentLocator(CreateProjectModal)
    project_created_modal = ComponentLocator(ProjectCreatedModal)


class AnalyticsPage(GuidBasePage):
    base_url = settings.OSF_HOME + '/{guid}/analytics/'

    identity = Locator(By.CSS_SELECTOR, '._Counts_1mhar6')
    private_project_message = Locator(By.CSS_SELECTOR, '._PrivateProject_1mhar6')
    disabled_chart = Locator(By.CSS_SELECTOR, '._Chart_1hff7g _Blurred_1hff7g')


class ForksPage(GuidBasePage):
    base_url = settings.OSF_HOME + '/{guid}/forks/'

    identity = Locator(By.CSS_SELECTOR, '._Forks_1xlord')
    new_fork_button = Locator(By.CSS_SELECTOR, '._Forks__new-fork_1xlord .btn-success')
    create_fork_modal_button = Locator(By.CSS_SELECTOR, '.modal-footer .btn-info')
    cancel_modal_button = Locator(By.CSS_SELECTOR, '.modal-footer .btn-default')
    info_toast = Locator(By.CSS_SELECTOR, '.toast-info')
    fork_link = Locator(By.CSS_SELECTOR, 'a[data-analytics-name="Title"]')
    fork_authors = Locator(By.CSS_SELECTOR, 'div[class="_NodeCard__authors_1i3kzz"]')
    placeholder_text = Locator(
        By.CSS_SELECTOR, 'div[class="_Forks__placeholder_1xlord"]'
    )

    # Group Locators
    listed_forks = GroupLocator(By.CSS_SELECTOR, '.list-group-item')


class FilesPage(GuidBasePage):
    base_url = settings.OSF_HOME + '/{guid}/files/{addon_provider}'

    def __init__(
        self, driver, verify=False, guid='', addon_provider='', domain=settings.OSF_HOME
    ):
        super().__init__(driver, verify)
        self.guid = guid
        self.addon_provider = addon_provider

    @property
    def url(self):
        if '{guid}' in self.base_url and '{addon_provider}' in self.base_url:
            return self.base_url.format(
                guid=self.guid, addon_provider=self.addon_provider
            )
        else:
            raise ValueError('No GUID or Addon Provider specified in base_url.')

    identity = Locator(By.CSS_SELECTOR, '[data-test-file-search]')
    session = osf_api.get_default_session()
    file_rows = GroupLocator(By.CSS_SELECTOR, '[data-test-file-list-item]')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-pulse')
    file_selected_text = Locator(By.CSS_SELECTOR, '[data-test-file-selected-count]')
    file_list_move_button = Locator(By.CSS_SELECTOR, '[data-test-bulk-move-trigger]')
    file_list_copy_button = Locator(By.CSS_SELECTOR, '[data-test-bulk-copy-trigger]')
    file_list_delete_button = Locator(
        By.CSS_SELECTOR, '[data-test-bulk-delete-trigger]'
    )
    leftnav_osfstorage_link = Locator(
        By.CSS_SELECTOR, '[data-test-files-provider-link="osfstorage"]'
    )

    # Components
    delete_modal = ComponentLocator(ConfirmFileDeleteModal)
    move_copy_modal = ComponentLocator(MoveCopyFileModal)
    rename_file_modal = ComponentLocator(RenameFileModal)


"""Note that the class FilesPage in pages/project.py is used for test_project_files.py.
The class FileWidget in components/project.py is used for tests test_file_widget_loads
and test_addon_files_load in test_project.py.
In the future, we may want to put all files tests in one place."""


class RegistrationsPage(GuidBasePage):
    base_url = settings.OSF_HOME + '/{guid}/registrations/'

    identity = Locator(By.CSS_SELECTOR, '[data-test-registrations-container]')
    registrations_tab = Locator(By.CSS_SELECTOR, 'ul._TabList_ojvago > li')
    draft_registrations_tab = Locator(By.CSS_SELECTOR, '[data-test-drafts-tab]')
    registration_card = Locator(By.CSS_SELECTOR, '[data-test-node-card]')
    draft_registration_card = Locator(
        By.CSS_SELECTOR, '[data-test-draft-registration-card]'
    )
    no_registrations_message_1 = Locator(
        By.CSS_SELECTOR,
        'div._RegistrationsPane_ojvago > div > div > div > div > p:nth-child(1)',
    )
    no_registrations_message_2 = Locator(
        By.CSS_SELECTOR,
        'div._RegistrationsPane_ojvago > div > div > div > div > p:nth-child(2)',
    )
    no_registrations_message_3 = Locator(
        By.CSS_SELECTOR,
        'div._RegistrationsPane_ojvago > div > div > div > div > p:nth-child(3)',
    )
    no_draft_registrations_message_1 = Locator(
        By.CSS_SELECTOR,
        'div._RegistrationsPane_ojvago > div > div > div > p:nth-child(1)',
    )
    no_draft_registrations_message_2 = Locator(
        By.CSS_SELECTOR,
        'div._RegistrationsPane_ojvago > div > div > div > p:nth-child(2)',
    )
    no_draft_registrations_message_3 = Locator(
        By.CSS_SELECTOR,
        'div._RegistrationsPane_ojvago > div > div > div > p:nth-child(3)',
    )
    here_support_link = Locator(By.LINK_TEXT, 'here')
    new_registration_button = Locator(
        By.CSS_SELECTOR, '[data-test-new-registration-button]'
    )
    # The following are for the first Draft Registration Card on the page. If we ever
    # deal with more than one draft registration card, then we should probably use
    # group locators and indexing.
    draft_registration_title = Locator(
        By.CSS_SELECTOR, 'h4[data-test-draft-registration-card-title] > a'
    )
    draft_registration_schema_name = Locator(
        By.CSS_SELECTOR, 'div[data-test-form-type] > dd'
    )
    draft_registration_provider = Locator(
        By.CSS_SELECTOR, 'div[data-test-provider-name] > dd'
    )
    review_draft_button = Locator(By.CSS_SELECTOR, '[data-test-draft-card-review]')
    edit_draft_button = Locator(By.CSS_SELECTOR, '[data-test-draft-card-edit]')
    delete_draft_button = Locator(
        By.CSS_SELECTOR, '[data-test-delete-button-secondary-destroy]'
    )
    # Components
    create_registration_modal = ComponentLocator(CreateRegistrationModal)
    delete_draft_registration_modal = ComponentLocator(
        ConfirmDeleteDraftRegistrationModal
    )
