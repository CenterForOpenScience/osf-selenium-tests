from selenium.webdriver.common.by import By

import settings
from base.locators import (
    ComponentLocator,
    GroupLocator,
    Locator,
)
from components.generic import SignUpForm
from components.navbars import EmberNavbar
from pages.base import OSFBasePage


class LandingPage(OSFBasePage):
    identity = Locator(By.CSS_SELECTOR, '._heroHeader_1qc5dv', settings.LONG_TIMEOUT)

    get_started_button = Locator(By.CSS_SELECTOR, '[data-test-get-started-button]')
    search_input = Locator(By.CSS_SELECTOR, '[data-test-search-input]')
    learn_more_button = Locator(
        By.CSS_SELECTOR, '[data-analytics-name="Learn more button"]'
    )
    testimonial_1_button = Locator(
        By.CSS_SELECTOR, '[data-analytics-name="Go to slide 1"]'
    )
    testimonial_2_button = Locator(
        By.CSS_SELECTOR, '[data-analytics-name="Go to slide 2"]'
    )
    testimonial_3_button = Locator(
        By.CSS_SELECTOR, '[data-analytics-name="Go to slide 3"]'
    )
    testimonial_1_slide = Locator(By.CSS_SELECTOR, '[data-test-testimonials-slide-1]')
    testimonial_2_slide = Locator(By.CSS_SELECTOR, '[data-test-testimonials-slide-2]')
    testimonial_3_slide = Locator(By.CSS_SELECTOR, '[data-test-testimonials-slide-3]')
    previous_testimonial_arrow = Locator(By.CSS_SELECTOR, '[data-test-previous-arrow]')
    next_testimonial_arrow = Locator(By.CSS_SELECTOR, '[data-test-next-arrow]')
    testimonial_view_research_links = GroupLocator(
        By.CSS_SELECTOR, '[data-analytics-name="View research"]'
    )

    # Components
    navbar = ComponentLocator(EmberNavbar)
    sign_up_form = ComponentLocator(SignUpForm)


class RegisteredReportsLandingPage(OSFBasePage):
    url = settings.OSF_HOME + '/rr/'

    identity = Locator(By.CSS_SELECTOR, '.reg-landing-page-logo')

    create_registered_report_button = Locator(
        By.CSS_SELECTOR,
        'body > div.watermarked > div > div > div.row.hidden-xs > table > tbody > tr:nth-child(1) > td > a > div',
    )
    cos_rr_link = Locator(
        By.CSS_SELECTOR,
        'body > div.watermarked > div > div > div:nth-child(8) > a:nth-child(1)',
    )
    osf_registries_link = Locator(
        By.CSS_SELECTOR,
        'body > div.watermarked > div > div > div:nth-child(8) > a:nth-child(2)',
    )
    cos_prereg_link = Locator(
        By.CSS_SELECTOR,
        'body > div.watermarked > div > div > div:nth-child(8) > a:nth-child(3)',
    )
