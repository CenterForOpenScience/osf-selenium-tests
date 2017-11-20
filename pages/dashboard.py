import settings

from selenium.webdriver.common.by import By
from pages.base import OSFBasePage, BaseElement, Locator

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
