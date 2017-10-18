import settings
import urllib.parse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# TODO: Find a clear distinction or rule for when I use a wait and when I don't
# TODO: Should I have seperate getters and setters/clicks
# Or if I'm only ever going to click is it okay to only have a click
# Or can the setting happen in the test - keep the pages objects pretty bare and just pass objects back to the test
class BasePage(object):
    url = None

    def __init__(self, driver):
        self.driver = driver

    def navigate(self):
        self.driver.get(self.url)

    def _wait_for_element(self, css):
        return WebDriverWait(
            driver=self.driver,
            timeout=settings.TIMEOUT
        ).until(
            method=EC.visibility_of_element_located(
                (By.CSS_SELECTOR, css)
            )
        )

# TODO: add something about needing to be logged in (otherwise this will be the landing pages)
class DashboardPage(BasePage):
    url = settings.DOMAIN

    def click_create_project(self):
        self._wait_for_element('button.btn-success:nth-child(1)').click()
        return CreateProjectModal(self.driver)


class CreateProjectModal(BasePage):

    def click_create_project(self):
        self._wait_for_element('#addProjectFromHome > div > div > div.modal-footer > button.btn.btn-success').click()
        return ProjectCreatedModal(self.driver)

    def set_title(self, title):
        self._wait_for_element('.form-control').send_keys(title)

    def click_more(self):
        self._wait_for_element('#addProjectFromHome > div > div > div.modal-body > div > div.text-muted.pointer').click()

    def click_select_all_institutions(self):
        self.driver.find_element_by_link_text('Select all').click()

    def click_remove_all_institutions(self):
        self.driver.find_element_by_link_text('Remove all').click()

    # TODO: Make this work for multiple and variable elements
    def institutions_selected(self):
        cos_logo = self.driver.find_element_by_css_selector(
            'div.form-group:nth-child(2) > table:nth-child(4) > tr:nth-child(1) > td:nth-child(1) > a:nth-child(1) > div:nth-child(1) > img:nth-child(1)')
        try:
            return not cos_logo.value_of_css_property('filter') == 'grayscale(100%)'
        except:
            return False

    def get_description_input(self):
        try:
            return self.driver.find_element_by_css_selector(
                '#addProjectFromHome > div > div > div.modal-body > div > div:nth-child(4) > input')
        except:
            return False

    def get_template_dropdown(self):
        try:
            return self.driver.find_element_by_id('select2-chosen-2')
        except:
            return False

    def click_cancel(self):
        self.driver.find_element_by_css_selector('#addProjectFromHome > div > div > div.modal-footer > button.btn.btn-default').click()

    def is_present(self):
        try:
            WebDriverWait(
                driver=self.driver,
                timeout=3
            ).until(
                method=EC.visibility_of_element_located(
                    (By.ID, 'addProjectFromHome')
                )
            )
            return True
        except:
            return False


class ProjectCreatedModal(BasePage):

    def click_go_to_project(self):
        self._wait_for_element('#addProjectFromHome > div > div > div > div.modal-footer > a').click()
        return ProjectPage(self.driver)

    def click_keep_working_here(self):
        self._wait_for_element('#addProjectFromHome > div > div > div > div.modal-footer > button').click()

class ProjectPage(BasePage):

    # It's optional to pass a project pages a guid.
    def __init__(self, driver, guid=''):
        super(self.__class__, self).__init__(driver)
        self.url = urllib.parse.urljoin(settings.DOMAIN, guid)

    def title_is(self, title):
        element = self._wait_for_element('#nodeTitleEditable')
        return element.text == title

