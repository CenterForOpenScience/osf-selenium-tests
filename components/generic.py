import settings

from time import sleep
from selenium.webdriver.common.by import By
from base.locators import Locator, BaseElement


class SignUpForm(BaseElement):
    name_input = Locator(By.NAME, 'fullName')
    email_one_input = Locator(By.NAME, 'email1')
    email_two_input = Locator(By.NAME, 'email2')
    password_input = Locator(By.NAME, 'password')
    terms_of_service_checkbox = Locator(By.NAME, 'acceptedTermsOfService')
    sign_up_button = Locator(By.CSS_SELECTOR, '[data-test-sign-up-button]')
    registration_success = Locator(By.CSS_SELECTOR, '.ext-success', settings.LONG_TIMEOUT)

    def click_recaptcha(self):
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name('iframe'))
        Locator(By.CSS_SELECTOR, '.recaptcha-checkbox-checkmark').get_element(self.driver, 'capcha').click()
        self.driver.switch_to.default_content()
        #TODO: Replace with an expected condition that checks if aria-checked="true"
        sleep(2)
