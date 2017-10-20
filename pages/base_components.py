import utils
import settings
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#TODO: If we go this route put this in a components folder
class BaseElement(object):
    TIMEOUT = settings.TIMEOUT

    def __init__(self):
        # self.driver = utils.launch_driver() #TODO: Make this work for me locally
        self.driver = settings.DRIVER #TODO: Make this work for me locally

    def _find_element(self, selector, locator, timeout=TIMEOUT):
        return WebDriverWait(
            driver=self.driver,
            timeout=timeout
        ).until(
            method=EC.visibility_of_element_located(
                (selector, locator)
            )
        )

    def _click_element(self, selector, locator, timeout=TIMEOUT):
        self._find_element(selector, locator, timeout).click()

    def _fill_element(self, selector, locator, value, timeout=TIMEOUT):
        self._find_element(selector, locator, timeout).send_keys(value)

    def _get_element_text(self, selector, locator, timeout=TIMEOUT):
        self._find_element(selector, locator, timeout).get_attribute('value')

class Navbar(BaseElement):
    sign_in_loc = (By.LINK_TEXT, 'Sign In')
    username_loc = (By.ID, 'username')
    password_loc = (By.ID, 'password')
    submit_loc = (By.NAME, 'submit')
    local_submit_loc = (By.ID, 'submit')
    remember_me_loc = (By.ID, 'rememberMe')
    user_dropdown_loc = (By.CSS_SELECTOR, '#secondary-navigation > ul > li:nth-child(5) > button')
    logout_link_loc = (By.CSS_SELECTOR, '#secondary-navigation > ul > li.dropdown.open > ul > li:nth-child(4) > a')

    def logged_in(self):
        try:
            self._find_element(*self.sign_in_loc)
            return False
        except:
            return True

    def login(self):
        if not self.logged_in():
            self._click_element(*self.sign_in_loc)
            self._fill_element(*self.username_loc, value=settings.USERNAME_ONE)
            if ("localhost:5000" in settings.DOMAIN):
                self._click_element(*self.local_submit_loc)
            else:
                self._fill_element(*self.password_loc, value=settings.PASSWORD)
                if (self._find_element(*self.remember_me_loc).is_selected()):
                    self._click_element(*self.remember_me_loc)
                self._click_element(*self.submit_loc)

    def logout(self):
        if self.logged_in():
            self._click_element(*self.user_dropdown_loc)
            self._click_element(*self.logout_link_loc)

