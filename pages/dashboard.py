from pages.project import ProjectPage
from pages.base import OSFBasePage, BaseElement
from selenium.webdriver.common.by import By


class DashboardPage(OSFBasePage):
    long_timeout = 30

    create_project_loc = (By.CSS_SELECTOR, 'button.btn-success:nth-child(1)')

    def __init__(self):
        super(DashboardPage, self).__init__()
        if not self.is_logged_in:
            raise ValueError

    def click_create_project(self):
        self._click_element(*self.create_project_loc, timeout=self.long_timeout)
        return CreateProjectModal()


class CreateProjectModal(BaseElement):
    #TODO: Possibly make these all element objects - that might be better and more efficient? Then I could get and set all of them for free
    modal_loc = (By.ID, 'addProjectFromHome')
    create_project_loc = (By.CSS_SELECTOR, '#addProjectFromHome > div > div > div.modal-footer > button.btn.btn-success')
    cancel_button_loc = (By.CSS_SELECTOR, '#addProjectFromHome > div > div > div.modal-footer > button.btn.btn-default')
    title_input_loc = (By.CSS_SELECTOR, '.form-control')
    select_all_loc = (By.LINK_TEXT, 'Select all')
    remove_all_loc = (By.LINK_TEXT, 'Remove all')
    more_pointer_loc = (By.CSS_SELECTOR, '#addProjectFromHome > div > div > div.modal-body > div > div.text-muted.pointer')
    description_input_loc = (By.CSS_SELECTOR, '#addProjectFromHome > div > div > div.modal-body > div > div:nth-child(4) > input')
    template_dropdown_loc = (By.ID, 'select2-chosen-2')

    def click_create_project(self):
        self._click_element(*self.create_project_loc)
        return ProjectCreatedModal()

    def set_title(self, title):
        self._fill_element(*self.title_input_loc, value=title)

    def click_more(self):
        self._click_element(*self.more_pointer_loc)

    def click_select_all_institutions(self):
        self._click_element(*self.select_all_loc)

    def click_remove_all_institutions(self):
        self._click_element(*self.remove_all_loc)

    def institutions_are_selected(self, institutions):
        try:
            for institution in institutions:
                logo = self._find_element(By.NAME, institution)
                return not logo.value_of_css_property('filter') == 'grayscale(100%)'
        except:
            return False

    def get_description_input(self):
        try:
            return self._find_element(*self.description_input_loc)
        except:
            return False

    def get_template_dropdown(self):
        try:
            return self._find_element(*self.template_dropdown_loc)
        except:
            return False

    def click_cancel(self):
        self._click_element(*self.cancel_button_loc)

    def is_present(self):
        try:
            self._find_element(*self.modal_loc)
            return True
        except:
            return False


class ProjectCreatedModal(BaseElement):
    go_to_project_loc = (By.CSS_SELECTOR, '#addProjectFromHome > div > div > div > div.modal-footer > a')
    keep_working_here_loc = (By.CSS_SELECTOR, '#addProjectFromHome > div > div > div > div.modal-footer > button')

    def click_go_to_project(self):
        self._click_element(*self.go_to_project_loc)
        return ProjectPage()

    def click_keep_working_here(self):
        self._click_element(*self.keep_working_here_loc)


