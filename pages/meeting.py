import settings
from pages.base import OSFBasePage, BaseElement
from selenium.webdriver.common.by import By


class MeetingPage(OSFBasePage):
    url = settings.OSF_HOME + '/meetings'

    locators = {
        'register': (By.CSS_SELECTOR, 'div.osf-meeting-header-img div.osf-meeting-header div button[data-target="#osf-meeting-register"]', settings.LONG_TIMEOUT),
        'upload': (By.CSS_SELECTOR, 'div.osf-meeting-header-img div.osf-meeting-header div button[data-target="#osf-meeting-upload"]', settings.LONG_TIMEOUT),
    }

    def __init__(self, driver):
        super(MeetingPage, self).__init__(driver)
        self.navbar = self.Navbar(driver)

    def _verify_page(self):
        return len(self.driver.find_element(By.CSS_SELECTOR, 'div.osf-meeting-header-img')) == 1

    class Navbar(BaseElement):

        locators = {
            'home': (By.XPATH, '//nav[@id="navbarScope"]/div/div[@class="navbar-header"]/div[@class="dropdown"]/ul[@role="menu"]/li/a[@href="' + settings.OSF_HOME + '"]'),
            'preprint': (By.XPATH, '//nav[@id="navbarScope"]/div/div[@class="navbar-header"]/div[@class="dropdown"]/ul[@role="menu"]/li/a[@href="' + settings.OSF_HOME + '/preprints/"]'),
            'registries': (By.XPATH, '//nav[@id="navbarScope"]/div/div[@class="navbar-header"]/div[@class="dropdown"]/ul[@role="menu"]/li/a[@href="' + settings.OSF_HOME + '/registries/"]'),
            'meetings': (By.XPATH, '//nav[@id="navbarScope"]/div/div[@class="navbar-header"]/div[@class="dropdown"]/ul[@role="menu"]/li/a[@href="' + settings.OSF_HOME + '/meetings/"]'),
            'search': (By.XPATH, '//div[@id="secondary-navigation"]/ul/li/a[@href="' + settings.OSF_HOME + '/search/"]'),
            'support': (By.XPATH, '//div[@id="secondary-navigation"]/ul/li/a[@href="/support/"]'),
            'donate': (By.XPATH, '//div[@id="secondary-navigation"]/ul/li/a[@href="https://cos.io/donate"]'),
            'user_dropdown': (By.CSS_SELECTOR, '#secondary-navigation > ul > li:nth-child(5) > button'),
            'user_dropdown_profile': (By.XPATH, '//div[@id="secondary-navigation"]/ul/li[@class="dropdown"]/ul/li/a[@href="/logout/"]'),
            'user_dropdown_support': (By.XPATH, '//div[@id="secondary-navigation"]/ul/li[@class="dropdown"]/ul/li/a[@href="' + settings.OSF_HOME + '/support/"]'),
            'user_dropdown_settings': (By.XPATH, '//div[@id="secondary-navigation"]/ul/li[@class="dropdown"]/ul/li/a[@href="/settings/"]'),
            'sign_up_button': (By.LINK_TEXT, 'Sign Up'),
            'sign_in_button': (By.LINK_TEXT, 'Sign In'),
            'logout_link': (By.CSS_SELECTOR, '#secondary-navigation > ul > li.dropdown.open > ul > li:nth-child(4) > a'),
            'current_service': (By.CSS_SELECTOR, '#navbarScope > div > div > div.service-home > a > span.current-service > strong')
        }

        def verify_element(self):
            return self.current_service.text == 'MEETINGS'

        def is_logged_in(self):
            try:
                if self.sign_in_button:
                    return False
            except ValueError:
                return True