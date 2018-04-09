import settings

from base.locators import BaseElement, Locator

from selenium.webdriver.common.by import By


class Navbar(BaseElement):
    service_dropdown = Locator(By.CSS_SELECTOR, '#navbarScope > div.container > div.navbar-header > div.dropdown > button')
    home_link = Locator(By.CSS_SELECTOR, '#navbarScope > div > div.navbar-header > div.dropdown.primary-nav.open > ul > li:nth-child(1) > a')
    preprints_link = Locator(By.CSS_SELECTOR, '#navbarScope > div.container > div.navbar-header > div.dropdown > ul > li:nth-child(2) > a')
    registries_link = Locator(By.CSS_SELECTOR, '#navbarScope > div.container > div.navbar-header > div.dropdown > ul > li:nth-child(3) > a')
    meetings_link = Locator(By.CSS_SELECTOR, '#navbarScope > div.container > div.navbar-header > div.dropdown > ul > li:nth-child(4) > a')
    search_link = Locator(By.XPATH, '//a[text()="Search"]')
    support_link = Locator(By.XPATH, '//a[text()="Support"]')
    donate_link = Locator(By.ID, 'navbar-donate')
    user_dropdown = Locator(By.CSS_SELECTOR, 'a.btn-link')
    user_dropdown_profile = Locator(By.CSS_SELECTOR, '#secondary-navigation > ul > li.dropdown.open > ul > li:nth-child(1) > a')
    user_dropdown_support = Locator(By.CSS_SELECTOR, '#secondary-navigation > ul > li.dropdown.open > ul > li:nth-child(2) > a')
    user_dropdown_settings = Locator(By.CSS_SELECTOR, '#secondary-navigation > ul > li.dropdown.open > ul > li:nth-child(3) > a')
    logout_link = Locator(By.CSS_SELECTOR, '#secondary-navigation > ul > li.dropdown.open > ul > li:nth-child(4) > a')
    sign_up_button = Locator(By.XPATH, '//a[text()="Sign Up"]')
    sign_in_button = Locator(By.LINK_TEXT, 'Sign In')
    current_service = Locator(By.CSS_SELECTOR, '#navbarScope .current-service > strong')

    def verify(self):
        return len(self.driver.find_elements(By.ID, 'navbarScope')) == 1

    def is_logged_in(self):
        return self.user_dropdown.present()

    def is_logged_out(self):
        return self.sign_in_button.present()


class HomeNavbar(Navbar):
    my_projects_link = Locator(By.XPATH, '//a[text()="My Projects"]')

    def verify(self):
        return self.current_service.text == 'HOME'


class AbstractLegacyEmberNavbar(Navbar):
    user_dropdown = Locator(By.CSS_SELECTOR, '#secondary-navigation > ul > li:nth-last-of-type(1) > a', settings.LONG_TIMEOUT)
    sign_in_button = Locator(By.CSS_SELECTOR, '#secondary-navigation > ul.nav > li.ember-view.dropdown.sign-in > a.btn.btn-info.btn-top-login', settings.LONG_TIMEOUT)


class PreprintsNavbar(AbstractLegacyEmberNavbar):
    add_a_preprint_link = Locator(By.CSS_SELECTOR, '#secondary-navigation > ul > li:nth-last-child(5) > a')

    def verify(self):
        return self.current_service.text == 'PREPRINTS'


class RegistriesNavbar(AbstractLegacyEmberNavbar):

    def verify(self):
        return self.current_service.text == 'REGISTRIES'

class MeetingsNavbar(Navbar):

    def verify(self):
        return self.current_service.text == 'MEETINGS'


class EmberNavbar(HomeNavbar):
    user_dropdown = Locator(By.CLASS_NAME, 'nav-profile-name')

    user_dropdown_profile = Locator(By.CSS_SELECTOR, '.dropdown-menu.auth-dropdown li:nth-child(1) > a')
    user_dropdown_support = Locator(By.CSS_SELECTOR, '.dropdown-menu.auth-dropdown li:nth-child(2) > a')
    user_dropdown_settings = Locator(By.CSS_SELECTOR, '.dropdown-menu.auth-dropdown li:nth-child(3) > a')
    logout_link = Locator(By.CSS_SELECTOR, '.dropdown-menu.auth-dropdown li:nth-child(4) > a')
    sign_in_button = Locator(By.CSS_SELECTOR, '.btn-top-login')
    donate_link = Locator(By.XPATH, '//a[text()="Donate"]')
