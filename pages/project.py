import settings

from selenium.webdriver.common.by import By

from api import osf_api
from components.project import FileWidget, LogWidget
from components.dashboard import CreateProjectModal, CreateCollectionModal, DeleteCollectionModal, ProjectCreatedModal
from pages.base import GuidBasePage, OSFBasePage
from base.locators import Locator, ComponentLocator, GroupLocator


class ProjectPage(GuidBasePage):

    identity = Locator(By.CSS_SELECTOR, '#overview > nav#projectSubnav')
    title = Locator(By.ID, 'nodeTitleEditable', settings.LONG_TIMEOUT)
    title_input = Locator(By.CSS_SELECTOR, '.form-inline input')
    title_edit_submit_button = Locator(By.CSS_SELECTOR, '.editable-submit')
    title_edit_cancel_button = Locator(By.CSS_SELECTOR, '.editable-cancel')
    make_public_link = Locator(By.XPATH, '//a[contains(text(), "Make Public")]')
    make_private_link = Locator(By.XPATH, '//a[contains(text(), "Make Private")]')
    confirm_privacy_change_link = Locator(By.XPATH, '//a[text()="Confirm"]')
    cancel_privacy_change_link = Locator(By.XPATH, '//a[text()="Cancel"]')

    # Components
    file_widget = ComponentLocator(FileWidget)
    log_widget = ComponentLocator(LogWidget)

class RequestAccessPage(GuidBasePage):

    identity = Locator(By.CSS_SELECTOR, '#requestAccessPrivateScope')


class MyProjectsPage(OSFBasePage):
    url = settings.OSF_HOME + '/myprojects/'

    identity = Locator(By.CSS_SELECTOR, '.col-xs-8 > h3:nth-child(1)')
    create_project_button = Locator(By.CSS_SELECTOR, '[data-target="#addProject"]')
    create_collection_button = Locator(By.CSS_SELECTOR, '[data-target="#addColl"]')
    first_custom_collection = Locator(By.CSS_SELECTOR, 'li[data-index="3"] span')
    first_collection_settings_button = Locator(By.CSS_SELECTOR, '.fa-ellipsis-v')
    first_collection_remove_button = Locator(By.CSS_SELECTOR, '[data-target="#removeColl"]')

    # Group Locators
    personal_collections = GroupLocator(By.CSS_SELECTOR, '.acceptDrop .ui-droppable')
    projects = GroupLocator(By.CSS_SELECTOR, '#projectOrganizer .fa-cube')

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

    # Group Locators
    listed_forks = GroupLocator(By.CSS_SELECTOR, '.list-group-item')

class FilesPage(GuidBasePage):
    base_url = settings.OSF_HOME + '/{guid}/files/'

    #TODO loading_indicator lives in FileWidget, don't repeat it here...
    identity = Locator(By.CSS_SELECTOR, '#treeGrid')
    loading_indicator = Locator(By.CSS_SELECTOR, '#treeGrid .ball-scale', settings.VERY_LONG_TIMEOUT)
    session = osf_api.get_default_session()
    fangorn_rows = GroupLocator(By.CSS_SELECTOR, '#tb-tbody .fg-file-links')
    fangorn_addons = GroupLocator(By.CSS_SELECTOR, '#tb-tbody .tb-odd')
    first_file = Locator(By.CSS_SELECTOR, '#tb-tbody .td-title[data-id~="4"]')
    file_action_buttons = GroupLocator(By.CSS_SELECTOR, '#folderRow .fangorn-toolbar-icon')
    delete_modal = Locator(By.CSS_SELECTOR, 'span.btn:nth-child(1)')
    checkout_modal = Locator(By.CSS_SELECTOR, 'a.btn:nth-child(2)')

    """first_file -- looking for the 4th row ensures that the files have loaded (in our test there will only ever be 1 header row,
    1 OSF Storage, and 1 additional addon in the widget, so the 4th row MUST be a file)"""
