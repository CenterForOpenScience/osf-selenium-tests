import settings
from pages.base import OSFBasePage, BaseElement
from selenium.webdriver.common.by import By


class DashboardPage(OSFBasePage):

    locators = dict(
        create_project_button=(By.CSS_SELECTOR, 'button.btn-success:nth-child(1)', settings.LONG_TIMEOUT),
        **OSFBasePage.locators
    )

    def __init__(self, driver, goto=True):
        super(DashboardPage, self).__init__(driver, goto)
        if not self.is_logged_in:
            raise ValueError

    def verify(self):
        return len(self.driver.find_elements(By.ID, 'osfHome')) == 1

    class CreateProjectModal(BaseElement):

        locators = {
            'modal': (By.ID, 'addProjectFromHome'),
            'create_project_button': (By.CSS_SELECTOR, '#addProjectFromHome > div > div > div.modal-footer > button.btn.btn-success'),
            'cancel_button': (By.CSS_SELECTOR, '#addProjectFromHome > div > div > div.modal-footer > button.btn.btn-default'),
            'title_input': (By.CSS_SELECTOR, '.form-control'),
            'select_all_link': (By.LINK_TEXT, 'Select all'),
            'remove_all_link': (By.LINK_TEXT, 'Remove all'),
            'more_arrow': (By.CSS_SELECTOR, '#addProjectFromHome > div > div > div.modal-body > div > div.text-muted.pointer'),
            'description_input': (By.CSS_SELECTOR, '#addProjectFromHome > div > div > div.modal-body > div > div:nth-child(4) > input'),
            'template_dropdown': (By.ID, 'select2-chosen-2'),
        }

        def institutions_are_selected(self, institutions):
            try:
                for institution in institutions:
                    logo = self.find_element(By.NAME, institution)
                    return not logo.value_of_css_property('filter') == 'grayscale(100%)'
            except:
                raise ValueError('Institution logo for {} not present in modal'.format(institution))

    class ProjectCreatedModal(BaseElement):

        locators = {
            'go_to_project_button': (By.CSS_SELECTOR, '#addProjectFromHome > div > div > div > div.modal-footer > a', settings.LONG_TIMEOUT),
            'keep_working_here_button': (By.CSS_SELECTOR, '#addProjectFromHome > div > div > div > div.modal-footer > button'),
        }
