import settings

from selenium.webdriver.common.by import By

from pages.base import OSFBasePage
from components.generic import SignUpForm
from components.navbars import EmberNavbar
from base.locators import Locator, ComponentLocator


class LandingPage(OSFBasePage):
    identity = Locator(By.CSS_SELECTOR, '._heroHeader_1qc5dv', settings.LONG_TIMEOUT)

    # Locators
    testimonial_carousel = Locator(By.CSS_SELECTOR, '[data-test-testimonials-container]')
    view_research = Locator(By.CSS_SELECTOR, 'a[data-analytics-name="View research"]')
    profile_page = Locator(By.CLASS_NAME, 'profile-fullname', settings.LONG_TIMEOUT)

    # Components
    navbar = ComponentLocator(EmberNavbar)
    sign_up_form = ComponentLocator(SignUpForm)

class RegisteredReportsLandingPage(OSFBasePage):
    url = settings.OSF_HOME + '/rr/'

    identity = Locator(By.CSS_SELECTOR, '.reg-landing-page-logo')
