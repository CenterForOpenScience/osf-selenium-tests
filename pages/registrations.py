from selenium.webdriver.common.by import By

import settings
from base.locators import Locator
from pages.base import OSFBasePage


class MyRegistrationsPage(OSFBasePage):
    url = settings.OSF_HOME + '/registries/my-registrations/'
    identity = Locator(
        By.CSS_SELECTOR, 'div[data-analytics-scope="My Registrations page"]'
    )

    drafts_tab = Locator(By.CSS_SELECTOR, '[data-test-my-registrations-nav="drafts"]')
    no_drafts_message = Locator(By.CSS_SELECTOR, 'p[data-test-draft-list-no-drafts]')
    create_a_registration_button_drafts = Locator(
        By.CSS_SELECTOR, 'a[data-test-my-reg-drafts-add-new-button]'
    )
    draft_registration_title = Locator(
        By.CSS_SELECTOR, 'a[data-analytics-name="view_registration"]'
    )

    submissions_tab = Locator(
        By.CSS_SELECTOR, '[data-test-my-registrations-nav="submitted"]'
    )
    no_submissions_message = Locator(
        By.CSS_SELECTOR, 'p[data-test-draft-list-no-registrations]'
    )
    create_a_registration_button_submitted = Locator(
        By.CSS_SELECTOR, 'a[data-test-my-reg-registrations-add-new-button]'
    )
    public_registration_title = Locator(By.CSS_SELECTOR, 'a[data-test-node-title]')

    update_button = Locator(By.CSS_SELECTOR, '[data-test-update-button]')
    update_registration_dialogue = Locator(By.CSS_SELECTOR, '[data-test-new-update-dialog-main]')
    update_registration_dialogue_next = Locator(By.CSS_SELECTOR, '[data-test-new-update-dialog-footer-next]')
