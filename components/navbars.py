from selenium.webdriver.common.by import By

from base.locators import (
    BaseElement,
    Locator,
)


# This is the navbar for legacy non-ember pages
class HomeNavbar(BaseElement):
    service_dropdown = Locator(By.CSS_SELECTOR, '.fa-caret-down')
    home_link = Locator(By.CSS_SELECTOR, 'a[data-analytics-name="HOME"]')
    preprints_link = Locator(By.CSS_SELECTOR, 'a[data-analytics-name="PREPRINTS"]')
    registries_link = Locator(By.CSS_SELECTOR, 'a[data-analytics-name="REGISTRIES"]')
    meetings_link = Locator(By.CSS_SELECTOR, 'a[data-analytics-name="MEETINGS"]')
    institutions_link = Locator(
        By.CSS_SELECTOR, 'a[data-analytics-name="INSTITUTIONS"]'
    )
    search_link = Locator(By.ID, 'navbar-search')
    support_link = Locator(By.ID, 'navbar-support')
    donate_link = Locator(By.ID, 'navbar-donate')

    user_dropdown = Locator(By.CSS_SELECTOR, '[data-test-auth-dropdown-toggle]')
    user_dropdown_profile = Locator(By.CSS_SELECTOR, '[data-test-ad-my-profile]')
    user_dropdown_support = Locator(By.CSS_SELECTOR, '[data-test-ad-support]')
    user_dropdown_settings = Locator(By.CSS_SELECTOR, '[data-test-ad-settings]')
    logout_link = Locator(By.CSS_SELECTOR, '[data-test-ad-logout]')

    sign_up_button = Locator(By.CSS_SELECTOR, 'a.btn-success:nth-child(1)')
    sign_in_button = Locator(By.CSS_SELECTOR, '.btn-top-login')
    current_service = Locator(By.CSS_SELECTOR, '#navbarScope .current-service > strong')

    def verify(self):
        return len(self.driver.find_elements(By.ID, 'navbarScope')) == 1

    def is_logged_in(self):
        return self.user_dropdown.present()

    def is_logged_out(self):
        return self.sign_in_button.present()


class EmberNavbar(HomeNavbar):
    search_link = Locator(By.CSS_SELECTOR, '[data-test-nav-search-link]')
    support_link = Locator(By.CSS_SELECTOR, '[data-test-nav-support-link]')
    donate_link = Locator(By.CSS_SELECTOR, '[data-test-nav-donate-link]')
    sign_up_button = Locator(By.CSS_SELECTOR, '[data-test-ad-sign-up-button]')
    sign_in_button = Locator(By.CSS_SELECTOR, '[data-test-sign-in-button]')

    user_dropdown = Locator(By.CSS_SELECTOR, '[data-test-auth-dropdown]')
    user_dropdown_profile = Locator(By.CSS_SELECTOR, '[data-test-ad-my-profile]')
    user_dropdown_support = Locator(By.CSS_SELECTOR, '[data-test-ad-support]')
    user_dropdown_settings = Locator(By.CSS_SELECTOR, '[data-test-ad-settings]')

    logout_link = Locator(By.CSS_SELECTOR, '[data-test-ad-logout]')
    my_projects_link = Locator(By.CSS_SELECTOR, '[data-test-nav-my-projects-link]')


class PreprintsNavbar(EmberNavbar):
    title = Locator(By.CSS_SELECTOR, '.navbar-title')

    home_link = Locator(By.CSS_SELECTOR, '[data-analytics-name="HOME"]')
    preprints_link = Locator(By.CSS_SELECTOR, '[data-analytics-name="PREPRINTS"]')
    registries_link = Locator(By.CSS_SELECTOR, '[data-analytics-name="REGISTRIES"]')
    meetings_link = Locator(By.CSS_SELECTOR, '[data-analytics-name="MEETINGS"]')
    institutions_link = Locator(By.CSS_SELECTOR, '[data-analytics-name="INSTITUTIONS"]')

    my_preprints_link = Locator(By.LINK_TEXT, 'My Preprints')
    my_reviewing_link = Locator(By.LINK_TEXT, 'My Reviewing')
    add_a_preprint_link = Locator(By.LINK_TEXT, 'Add a Preprint')
    search_link = Locator(By.LINK_TEXT, 'Search')
    support_link = Locator(By.LINK_TEXT, 'Support')
    donate_link = Locator(By.LINK_TEXT, 'Donate')
    sign_up_button = Locator(By.LINK_TEXT, 'Sign Up')
    sign_in_button = Locator(By.LINK_TEXT, 'Sign In')

    # Request a new locator from devs
    user_dropdown = Locator(By.CSS_SELECTOR, '.nav-profile-name')
    user_dropdown_profile = Locator(By.LINK_TEXT, 'My Profile')
    user_dropdown_support = Locator(By.LINK_TEXT, 'OSF Support')
    user_dropdown_settings = Locator(By.LINK_TEXT, 'Settings')
    logout_link = Locator(By.LINK_TEXT, 'Log Out')

    def verify(self):
        return self.current_service.text == 'PREPRINTS'


class RegistriesNavbar(EmberNavbar):
    home_link = Locator(By.CSS_SELECTOR, 'a[data-analytics-name="HOME"]')
    preprints_link = Locator(By.CSS_SELECTOR, 'a[data-analytics-name="PREPRINTS"]')
    registries_link = Locator(By.CSS_SELECTOR, 'a[data-analytics-name="REGISTRIES"]')
    meetings_link = Locator(By.CSS_SELECTOR, 'a[data-analytics-name="MEETINGS"]')
    institutions_link = Locator(
        By.CSS_SELECTOR, 'a[data-analytics-name="INSTITUTIONS"]'
    )

    help_link = Locator(By.CSS_SELECTOR, 'a[data-test-help]')
    donate_link = Locator(By.CSS_SELECTOR, 'a[data-test-donate]')
    join_link = Locator(By.CSS_SELECTOR, 'a[data-test-join]')
    login_link = Locator(By.CSS_SELECTOR, 'a[data-test-login]')

    # For Registries Only -> This clicks the gravatar image. (Same effect)
    user_dropdown = Locator(By.CSS_SELECTOR, 'img[data-test-gravatar]')

    add_new_link = Locator(
        By.CSS_SELECTOR, 'a[data-test-add-new-button][href="/registries/osf/new"]'
    )
    my_registrations_link = Locator(
        By.CSS_SELECTOR,
        'a[data-test-add-new-button][href="/registries/my-registrations"]',
    )

    def verify(self):
        return self.current_service.text == 'REGISTRIES'


class MeetingsNavbar(EmberNavbar):
    def verify(self):
        return self.current_service.text == 'MEETINGS'


class InstitutionsNavbar(EmberNavbar):
    def verify(self):
        return self.current_service.text == 'INSTITUTIONS'


class CollectionsNavbar(EmberNavbar):
    title = Locator(By.CSS_SELECTOR, '.navbar-title')
