import settings

from selenium.webdriver.common.by import By
from pages.base import (
    OSFBasePage,
    BaseElement,
    Locator,
)

class DashboardPage(OSFBasePage):

    # Locators
    identity = Locator(By.CSS_SELECTOR, '#osfHome > div.prereg-banner', settings.LONG_TIMEOUT)
    create_project_button = Locator(By.CSS_SELECTOR, 'button.btn-success:nth-child(1)', settings.LONG_TIMEOUT)

    def __init__(self, driver, verify=False):
        super(DashboardPage, self).__init__(driver, verify, require_login=True)

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

        def institutions_are_selected(self, institutions):
            try:
                for institution in institutions:
                    logo = self.find_element(By.NAME, institution)
                    return not logo.value_of_css_property('filter') == 'grayscale(100%)'
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

        def get_nth_project(self, driver, n=1):
            base_selector = 'div.quick-search-table > div:nth-child(3) > a:nth-child'
            try:
                selector = '{}({})'.format(base_selector, n)
                element = driver.find_element(By.CSS_SELECTOR, selector)
                guid = element.get_attribute('href').strip('/')
                return {'guid': guid, 'selector': selector}
            except:
                raise ValueError('Unable to find a project at position {}'.format(n))

        def get_list_length(self, driver):
            project_list_selector = 'div.quick-search-table > div:nth-child(3) > a'
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, project_list_selector)
                return len(elements)
            except:
                raise ValueError('Unable to get the length of project list')
