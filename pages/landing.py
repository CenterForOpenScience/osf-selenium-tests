import settings

from selenium.webdriver.common.by import By

from pages.base import OSFBasePage
from components.navbars import EmberNavbar
from base.locators import Locator, ComponentLocator


class LandingPage(OSFBasePage):
    identity = Locator(By.ID, 'home-hero', settings.LONG_TIMEOUT)

    name_input = Locator(By.NAME, 'fullName')
    email_one_input = Locator(By.NAME, 'email1')
    email_two_input = Locator(By.NAME, 'email2')
    password_input = Locator(By.NAME, 'password')
    terms_of_service_checkbox = Locator(By.NAME, 'acceptedTermsOfService')
    sign_up_button = Locator(By.CSS_SELECTOR, '._SignUpForm_3ntsx4 .btn-success')
    registration_success = Locator(By.CSS_SELECTOR, '.ext-success', settings.LONG_TIMEOUT)

    # Components
    navbar = ComponentLocator(EmberNavbar)


class LegacyLandingPage(OSFBasePage):
    waffle_override = {'ember_home_page': LandingPage}

    identity = Locator(By.ID, 'home-hero', settings.LONG_TIMEOUT)
