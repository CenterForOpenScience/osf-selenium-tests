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
from components.helpers import format_addon_name
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
    alert_info_message = Locator(By.CSS_SELECTOR, 'div.subhead > div.alert.alert-info')
    parent_project_link = Locator(By.CSS_SELECTOR, 'h2.node-parent-title > a')
    description = Locator(By.ID, 'nodeDescriptionEditable')
    contributors_list = Locator(By.CSS_SELECTOR, '#contributorsList > ol')
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

    # Navigate to the Project Overview page if you are not already on it
    project_page = ProjectPage(driver, guid=node_id)
    if project_page.identity.absent():
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

    # Look for the appropriate log entry in the api data
    for entry in logs:
        if entry['attributes']['action'] == action:
            log_data = entry
            log_params = entry['attributes']['params']
            break

    # Verify relevant details specific to the log action type
    if 'file_removed' in action:
        # For File Deletion actions
        file_name = kwargs.get('file_name')
        provider = format_addon_name(kwargs.get('provider'))
        # Verify file name is in the path parameter attribute
        assert file_name in log_params['path']
        # Build the expected text string to find in the Log Widget text line
        # EX: 'removed file delete_chrome_box.txt from Box'
        if provider == 'Amazon S3':
            log_text = 'removed {} in {} bucket'.format(file_name, provider)
        else:
            log_text = 'removed file {} from {}'.format(file_name, provider)
    elif action == 'addon_file_moved' or action == 'addon_file_copied':
        # For File Move or Copy actions
        file_name = kwargs.get('file_name')
        source = format_addon_name(kwargs.get('source'))
        destination = format_addon_name(kwargs.get('destination'))
        # Verify move or copy specific attributes in the api log entry
        assert log_params['destination']['materialized'] == file_name
        assert log_params['destination']['addon'] == destination
        assert log_params['source']['materialized'] == file_name
        assert log_params['source']['addon'] == source
        # Build the expected text string to find in the Log Widget text line
        # EX: 'moved move_chrome_box.txt in Box to move_chrome_box.txt in OSF Storage'
        log_text = '{} {} in {} to {} in {}'.format(
            action[11:], file_name, source, file_name, destination
        )
    elif action == 'addon_file_renamed':
        # For File Rename actions
        file_name = kwargs.get('file_name')
        renamed_file = kwargs.get('renamed_file')
        source = format_addon_name(kwargs.get('source'))
        destination = format_addon_name(kwargs.get('destination'))
        # Verify rename specific attributes in the api log entry
        assert log_params['destination']['materialized'] == renamed_file
        assert log_params['destination']['addon'] == destination
        assert log_params['source']['materialized'] == file_name
        assert log_params['source']['addon'] == source
        # Build the expected text string to find in the Log Widget text line
        # EX: 'renamed rename_chrome_box.txt in Box to chrome_box_renamed.txt in Box'
        log_text = 'renamed {} in {} to {} in {}'.format(
            file_name, source, renamed_file, destination
        )
    elif action == 'view_only_link_added':
        # For VOLs or AVOLs, although we are not going to verify the log entries for
        # AVOLs since they are generally pointless and don't give enough information
        # to be worthwhile to anyone. EX: 'A user created a view-only link to a project'
        anonymous = kwargs.get('anonymous')
        assert log_params['anonymous_link'] == anonymous
        log_text = 'created a view-only link to'
    elif action == 'edit_title':
        # For changing the Title on a Project
        orig_title = kwargs.get('orig_title')
        new_title = kwargs.get('new_title')
        assert log_params['title_original'] == orig_title
        assert log_params['title_new'] == new_title
        log_text = 'changed the title from {} to {}'.format(orig_title, new_title)
    elif action == 'made_public':
        # For making a Project node Public
        log_text = 'made {} public'.format(project_title)
    elif action == 'node_forked':
        # For a node that has been Forked from another Project node
        orig_guid = kwargs.get('orig_guid')
        orig_title = kwargs.get('orig_title')
        assert log_params['params_node']['id'] == orig_guid
        assert log_params['params_node']['title'] == orig_title
        log_text = 'created fork from {}'.format(orig_title)
        # override project_title since the log entry has title of the original project
        # node not the new forked node
        project_title = orig_title
    elif action == 'affiliated_institution_added':
        # For when a Project is affiliated with an institution. Typically this happens
        # upon creation of the node.
        node_guid = kwargs.get('node_guid')
        node_title = kwargs.get('node_title')
        institution_name = kwargs.get('institution_name')
        assert log_params['params_node']['id'] == node_guid
        assert log_params['params_node']['title'] == node_title
        assert log_params['institution']['name'] == institution_name
        log_text = 'added {} affiliation to {}'.format(institution_name, node_title)
    elif action == 'project_created':
        # For the creation of a new Project or Component node
        node_guid = kwargs.get('node_guid')
        node_title = kwargs.get('node_title')
        assert log_params['params_node']['id'] == node_guid
        assert log_params['params_node']['title'] == node_title
        log_text = 'created {}'.format(node_title)
        # Need to override the log item text with the 2nd log item row since the first
        # log item row is always the add affiliation log entry whenever we create a new
        # project or node in OSF.
        log_item_1_text = project_page.log_widget.log_items[1].text
    elif action == 'node_removed':
        # For the deletion of a Component node from a Project
        node_guid = kwargs.get('node_guid')
        node_title = kwargs.get('node_title')
        assert log_params['params_node']['id'] == node_guid
        assert log_params['params_node']['title'] == node_title
        log_text = 'removed {}'.format(node_title)
        # override project_title since the log entry has title of the component node
        # not the parent project
        project_title = node_title

    # Verify the text displayed in the Log Widget
    assert log_text in log_item_1_text

    # The following data should be in all log entries:
    # Verify the log entry begins with the user name
    user = osf_api.current_user()
    assert log_item_1_text.startswith(user.full_name)
    assert log_data['relationships']['user']['data']['id'] == user.id
    # Verify project title is in the log entry
    assert project_title in log_item_1_text
    assert log_params['params_node']['title'] == project_title
    # Verify current date is also in the log entry
    now = datetime.now()
    utc_now = datetime.utcnow()

    # The front end uses whatever time zone your web browser is synced to
    date_today = now.strftime('%Y-%m-%d')
    assert date_today in log_item_1_text
    assert date_today in log_data['attributes']['date']

    # The API logs time in UTC
    utc_date_today = utc_now.strftime('%Y-%m-%d')
    assert utc_date_today in log_data['attributes']['date']


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

    identity = Locator(
        By.CSS_SELECTOR, '[data-test-analytics-page-heading]', settings.LONG_TIMEOUT
    )
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-pulse')
    private_project_message = Locator(By.CSS_SELECTOR, '._private-project_1mhar6')
    disabled_chart = Locator(By.CSS_SELECTOR, '._Chart_1hff7g _Blurred_1hff7g')

    unique_visits_week_current_day_point = Locator(
        By.CSS_SELECTOR, 'circle.c3-shape.c3-shape-7.c3-circle.c3-circle-7'
    )
    unique_visits_tooltip_value = Locator(
        By.CSS_SELECTOR,
        'div._ChartContainer_1hff7g._panel-body_1hff7g > div > div > table > tbody > tr.c3-tooltip-name--count > td.value',
    )
    tod_visits_tooltip_value = Locator(
        By.CSS_SELECTOR,
        'div[data-test-analytics-page-heading] > div:nth-child(3) > div > div:nth-child(2) > div > div._ChartContainer_1hff7g._panel-body_1hff7g > div > div > table > tbody > tr.c3-tooltip-name--count > td.value',
    )
    most_visited_page_label = Locator(
        By.CSS_SELECTOR,
        'div[data-test-analytics-page-heading] > div:nth-child(3) > div > div:nth-child(4) > div > div._ChartContainer_1hff7g._panel-body_1hff7g > div > svg > g:nth-child(2) > g.c3-axis.c3-axis-x > g:nth-child(2) > text > tspan',
    )
    most_visited_page_bar = Locator(
        By.CSS_SELECTOR,
        'div[data-test-analytics-page-heading]> div:nth-child(3) > div > div:nth-child(4) > div > div._ChartContainer_1hff7g._panel-body_1hff7g > div > svg > g:nth-child(2) > g.c3-chart > g.c3-chart-bars > g > g > path.c3-shape.c3-shape-0.c3-bar.c3-bar-0',
    )
    popular_pages_tooltip_value = Locator(
        By.CSS_SELECTOR,
        'div.container._page-container_1mhar6 > div:nth-child(3) > div > div:nth-child(4) > div > div._ChartContainer_1hff7g._panel-body_1hff7g > div > div > table > tbody > tr.c3-tooltip-name--count > td.value',
    )

    tod_bars = GroupLocator(
        By.CSS_SELECTOR,
        'div[data-test-analytics-page-heading] > div:nth-child(3) > div > div:nth-child(2) > div > div._ChartContainer_1hff7g._panel-body_1hff7g > div > svg > g:nth-child(2) > g.c3-chart > g.c3-chart-bars > g > g > path',
    )

    def get_tod_bar_by_hour(self, hour):
        for bar in self.tod_bars:
            if 'bar-' + str(hour) in bar.get_attribute('class'):
                return bar


class ForksPage(GuidBasePage):
    base_url = settings.OSF_HOME + '/{guid}/forks/'

    identity = Locator(By.CSS_SELECTOR, '._Forks_1xlord')
    project_title = Locator(By.CSS_SELECTOR, 'div.ember-view._Hero_widcfp > h1')
    new_fork_button = Locator(By.CSS_SELECTOR, '[data-test-new-fork-button]')
    create_fork_modal_button = Locator(
        By.CSS_SELECTOR, '[data-test-confirm-create-fork]'
    )
    cancel_modal_button = Locator(By.CSS_SELECTOR, '[data-test-cancel-create-fork]')
    info_toast = Locator(By.CSS_SELECTOR, '.toast-info')
    fork_link = Locator(By.CSS_SELECTOR, 'a[data-analytics-name="Title"]')
    fork_authors = Locator(By.CSS_SELECTOR, '[data-test-contributor-name]')
    placeholder_text = Locator(
        By.CSS_SELECTOR, 'div[class="_Forks__placeholder_1xlord"]'
    )

    # Group Locators
    listed_forks = GroupLocator(By.CSS_SELECTOR, '[data-test-node-card]')


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
    alert_info_message = Locator(By.CSS_SELECTOR, 'div._banner_1acc8u > p')
    leave_vol_button = Locator(By.CSS_SELECTOR, '[data-test-view-normally]')
    file_rows = GroupLocator(By.CSS_SELECTOR, '[data-test-file-list-item]')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-pulse')
    add_file_folder_button = Locator(By.CSS_SELECTOR, '[data-test-add-new-trigger]')
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
    registrations_tab = Locator(By.CSS_SELECTOR, 'ul._tab-list_ojvago > li')
    draft_registrations_tab = Locator(By.CSS_SELECTOR, '[data-test-drafts-tab]')
    registration_card = Locator(By.CSS_SELECTOR, '[data-test-node-card]')
    draft_registration_card = Locator(
        By.CSS_SELECTOR, '[data-test-draft-registration-card]'
    )
    no_registrations_message_1 = Locator(
        By.CSS_SELECTOR,
        'div[data-test-registrations-pane] > div > div > div > div > div > p:nth-child(1)',
    )
    no_registrations_message_2 = Locator(
        By.CSS_SELECTOR,
        'div[data-test-registrations-pane] > div > div > div > div > div > p:nth-child(2)',
    )
    no_registrations_message_3 = Locator(
        By.CSS_SELECTOR,
        'div[data-test-registrations-pane] > div > div > div > div > div > p:nth-child(3)',
    )
    no_draft_registrations_message_1 = Locator(
        By.CSS_SELECTOR,
        'div[data-test-draft-registrations-pane] > div > div > div > div > p:nth-child(1)',
    )
    no_draft_registrations_message_2 = Locator(
        By.CSS_SELECTOR,
        'div[data-test-draft-registrations-pane] > div > div > div > div > p:nth-child(2)',
    )
    no_draft_registrations_message_3 = Locator(
        By.CSS_SELECTOR,
        'div[data-test-draft-registrations-pane] > div > div > div > div > p:nth-child(3)',
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
