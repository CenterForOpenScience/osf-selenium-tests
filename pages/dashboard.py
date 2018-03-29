import settings
from time import sleep

from selenium.webdriver.common.by import By
from pages.base import (
    OSFBasePage,
    BaseElement,
    Locator,
    GroupLocator
)

class EmberDashboardPage(OSFBasePage):

    # Locators
    identity = Locator(By.CSS_SELECTOR, '.__35060.Application__page > div.quickSearch > div > div > div > div > div:nth-child(1) > h2', settings.LONG_TIMEOUT)
    create_project_button = Locator(By.CSS_SELECTOR, '.__35060.Application__page > div.quickSearch > div > div > div > div > div:nth-child(1) > div > div > button', settings.LONG_TIMEOUT)
    view_meetings_button = Locator(By.LINK_TEXT, 'View meetings')
    view_preprints_button = Locator(By.LINK_TEXT, 'View preprints')
    start_prereg_button = Locator(By.LINK_TEXT, 'Start Prereg Challenge')
    first_popular_project_entry = Locator(By.CLASS_NAME, '__66865', settings.LONG_TIMEOUT)

    class CreateProjectModal(BaseElement):

        # Locators
        modal = Locator(By.CLASS_NAME, 'modal-dialog')
        create_project_button = Locator(By.CSS_SELECTOR, 'button.btn:nth-child(2)')
        cancel_button = Locator(By.CSS_SELECTOR, 'button.btn:nth-child(1)')
        title_input = Locator(By.CLASS_NAME, 'form-control')
        select_all_link = Locator(By.LINK_TEXT, 'Select all')
        remove_all_link = Locator(By.LINK_TEXT, 'Remove all')
        more_arrow = Locator(By.CLASS_NAME, 'fa')
        description_input = Locator(By.CLASS_NAME, 'project-desc')
        template_dropdown = Locator(By.CLASS_NAME, 'ember-power-select-placeholder')

        def institution_selected(self, institution):
            try:
                logo = self.modal.find_element_by_name(institution)
                return '0.25' not in logo.value_of_css_property('opacity')
            except:
                raise ValueError('Institution logo for {} not present in modal'.format(institution))

    class ProjectCreatedModal(BaseElement):

        # Locators
        go_to_project_button = Locator(By.LINK_TEXT, 'Go to new project', settings.LONG_TIMEOUT)
        keep_working_here_button = Locator(By.CSS_SELECTOR, 'button.btn-default')

    class ProjectList(BaseElement):

        # Locators
        search_input = Locator(By.CSS_SELECTOR, '.__35060.Application__page > div.quickSearch input')
        top_project_link = Locator(By.CLASS_NAME, 'DashboardItem')
        sort_title_asc_button = Locator(By.CSS_SELECTOR, '.__35060 .quick-search-table > div.row.node-col-headers.m-t-md > div.col-sm-3.col-md-6 > div > span > button:nth-child(1)')
        sort_title_dsc_button = Locator(By.CSS_SELECTOR, '.__35060 .quick-search-table > div.row.node-col-headers.m-t-md > div.col-sm-3.col-md-6 > div > span > button:nth-child(2)')
        sort_date_asc_button = Locator(By.CSS_SELECTOR, '.__35060 .quick-search-table > div.row.node-col-headers.m-t-md > div:nth-child(3) > div > span > button:nth-child(1)')
        sort_date_dsc_button = Locator(By.CSS_SELECTOR, '.__35060 .quick-search-table > div.row.node-col-headers.m-t-md > div:nth-child(3) > div > span > button:nth-child(2)')
        loading_dashboard_item = Locator(By.CLASS_NAME, 'loading-dashboard-item', settings.QUICK_TIMEOUT)

        # Group Locators
        project_list_projects = GroupLocator(By.CSS_SELECTOR, '.__3eb7f > a')

        def get_nth_project_link(self, n=0):
            if self.loading_dashboard_item.here_then_gone():
                try:
                    element = self.project_list_projects[n - 1]
                    return element.get_attribute('href')
                except IndexError:
                    raise ValueError('Unable to find a project at position {}'.format(n))
            raise ValueError('Dashboard page is still loading.')

        def get_list_length(self):
            if self.loading_dashboard_item.here_then_gone():
                return len(self.project_list_projects)
            raise ValueError('Dashboard page is still loading.')


class DashboardPage(OSFBasePage):
    url = settings.OSF_HOME + '/dashboard'

    waffle_override = {'ember_home_page': EmberDashboardPage}

    # Locators
    identity = Locator(By.CSS_SELECTOR, '#osfHome > div.prereg-banner', settings.LONG_TIMEOUT)
    create_project_button = Locator(By.CSS_SELECTOR, 'button.btn-success:nth-child(1)', settings.LONG_TIMEOUT)
    view_meetings_button = Locator(By.LINK_TEXT, 'View meetings')
    view_preprints_button = Locator(By.LINK_TEXT, 'View preprints')
    start_prereg_button = Locator(By.LINK_TEXT, 'Start Prereg Challenge')
    new_and_noteworthy = Locator(By.CSS_SELECTOR, '#osfHome > div.newAndNoteworthy > div > div:nth-child(2) > div > div > div:nth-child(1) > div:nth-child(1) > div > h4', settings.LONG_TIMEOUT)
    first_popular_project_entry = Locator(By.CLASS_NAME, 'public-projects-item', settings.LONG_TIMEOUT)
    popular_projects = Locator(By.CSS_SELECTOR, '#osfHome > div.newAndNoteworthy > div > div:nth-child(2) > div > div > div:nth-child(1) > div:nth-child(2) > div > h4', settings.LONG_TIMEOUT)
    institutions_carousel_left_arrow = Locator(By.CSS_SELECTOR, '.left.carousel-control')
    institutions_carousel_right_arrow = Locator(By.CSS_SELECTOR, '.right.carousel-control')

    # Group locators
    institution_carousel_logos = GroupLocator(By.CLASS_NAME, 'img-circle')

    def get_institutions(self):
        page_institutions = self.institution_carousel_logos
        if self.institutions_carousel_left_arrow.absent():
            return page_institutions
        while True:
            self.institutions_carousel_right_arrow.click()
            for logo in self.institution_carousel_logos:
                if logo in page_institutions:
                    return page_institutions
                page_institutions.append(logo)
            return page_institutions

    class CreateProjectModal(BaseElement):

        # Locators
        modal = Locator(By.ID, 'addProjectFromHome')
        create_project_button = Locator(By.CSS_SELECTOR, '#addProjectFromHome > div > div > div.modal-footer > button.btn.btn-success')
        cancel_button = Locator(By.CSS_SELECTOR, '#addProjectFromHome > div > div > div.modal-footer > button.btn.btn-default')
        title_input = Locator(By.CSS_SELECTOR, '.form-control')
        select_all_link = Locator(By.LINK_TEXT, 'Select all')
        remove_all_link = Locator(By.LINK_TEXT, 'Remove all')
        more_arrow = Locator(By.CSS_SELECTOR, '#addProjectFromHome > div > div > div.modal-body > div > div.text-muted.pointer')
        description_input = Locator(By.CSS_SELECTOR, '#addProjectFromHome > div > div > div.modal-body > div > div:nth-child(4) > input')
        template_dropdown = Locator(By.ID, 'select2-chosen-2')

        def institution_selected(self, institution):
            try:
                logo = self.modal.find_element(By.NAME, institution)
                return '0.25' not in logo.value_of_css_property('opacity')
            except:
                raise ValueError('Institution logo for {} not present in modal'.format(institution))

    class ProjectCreatedModal(BaseElement):

        # Locators
        go_to_project_button = Locator(By.CSS_SELECTOR, '#addProjectFromHome > div > div > div > div.modal-footer > a', settings.LONG_TIMEOUT)
        keep_working_here_button = Locator(By.CSS_SELECTOR, '#addProjectFromHome > div > div > div > div.modal-footer > button')

    class ProjectList(BaseElement):

        # Locators
        search_input = Locator(By.ID, 'searchQuery')
        top_project_link = Locator(By.CSS_SELECTOR, 'div.quick-search-table > div:nth-child(3) > a:nth-child(1)')
        sort_title_asc_button = Locator(By.CSS_SELECTOR,
            'div.quick-search-table > div.row.node-col-headers.m-t-md > div.col-sm-3.col-md-6 > div > button:nth-child(1)')
        sort_title_dsc_button = Locator(By.CSS_SELECTOR,
            'div.quick-search-table > div.row.node-col-headers.m-t-md > div.col-sm-3.col-md-6 > div > button:nth-child(2)')
        sort_date_asc_button = Locator(By.CSS_SELECTOR,
            'div.quick-search-table > div.row.node-col-headers.m-t-md > div:nth-child(3) > div > span > button:nth-child(1)')
        sort_date_dsc_button = Locator(By.CSS_SELECTOR,
            'div.quick-search-table > div.row.node-col-headers.m-t-md > div:nth-child(3) > div > span > button:nth-child(2)')

        # Group Locators
        project_list_projects = GroupLocator(By.CSS_SELECTOR, 'div.quick-search-table > div:nth-child(3) > a')

        # TODO: Refactor to use a locator
        def get_nth_project_guid(self, n=0):
            base_selector = 'div.quick-search-table > div:nth-child(3) > a:nth-child'
            try:
                selector = '{}({})'.format(base_selector, n)
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                guid = element.get_attribute('href').strip('/')
                return guid
            except:
                raise ValueError('Unable to find a project at position {}'.format(n))

        def get_list_length(self):
            sleep(0.4)  # Need sleep to let quicksearch do its thing
            return len(self.project_list_projects)
