import settings

from selenium.webdriver.common.by import By

import components.dashboard as components

from pages.base import OSFBasePage
from components.navbars import EmberNavbar
from base.locators import Locator, GroupLocator, ComponentLocator


class BaseDashboardPage(OSFBasePage):
    # TODO: Write in mandatory locators?

    def get_institutions(self):
        page_institutions = self.institution_carousel_logos
        if self.institutions_carousel_left_arrow.absent():
            return page_institutions
        while True:
            self.institutions_carousel_right_arrow.click()
            for logo in self.institution_carousel_logos:
                if logo in page_institutions:
                    return page_institutions
                page_institutions.append(logo)
            return page_institutions


class EmberDashboardPage(BaseDashboardPage):
    url = settings.OSF_HOME + '/dashboard/'

    identity = Locator(By.CSS_SELECTOR, '.__35060.Application__page > div.quickSearch > div > div > div > div > div:nth-child(1) > h2', settings.LONG_TIMEOUT)
    create_project_button = Locator(By.CSS_SELECTOR, '.__35060.Application__page > div.quickSearch > div > div > div > div > div:nth-child(1) > div > div > button', settings.LONG_TIMEOUT)
    view_meetings_button = Locator(By.LINK_TEXT, 'View meetings')
    view_preprints_button = Locator(By.LINK_TEXT, 'View preprints')
    start_prereg_button = Locator(By.LINK_TEXT, 'Start Prereg Challenge')
    first_popular_project_entry = Locator(By.CLASS_NAME, '__66865', settings.LONG_TIMEOUT)
    institutions_carousel_left_arrow = Locator(By.CSS_SELECTOR, '.left.carousel-control')
    institutions_carousel_right_arrow = Locator(By.CSS_SELECTOR, '.right.carousel-control')

    # Group locators
    institution_carousel_logos = GroupLocator(By.CLASS_NAME, 'InstitutionCarousel__item__image')

    # Components
    navbar = ComponentLocator(EmberNavbar)
    create_project_modal = ComponentLocator(components.EmberCreateProjectModal)
    project_created_modal = ComponentLocator(components.EmberProjectCreatedModal)
    project_list = ComponentLocator(components.EmberProjectList)


class DashboardPage(BaseDashboardPage):
    waffle_override = {'ember_home_page': EmberDashboardPage}

    identity = Locator(By.CSS_SELECTOR, '#osfHome > div.prereg-banner', settings.LONG_TIMEOUT)
    create_project_button = Locator(By.CSS_SELECTOR, 'button.btn-success:nth-child(1)', settings.LONG_TIMEOUT)
    view_meetings_button = Locator(By.LINK_TEXT, 'View meetings')
    view_preprints_button = Locator(By.LINK_TEXT, 'View preprints')
    start_prereg_button = Locator(By.LINK_TEXT, 'Start Prereg Challenge')
    new_and_noteworthy = Locator(By.CSS_SELECTOR, '#osfHome > div.newAndNoteworthy > div > div:nth-child(2) > div > div > div:nth-child(1) > div:nth-child(1) > div > h4', settings.LONG_TIMEOUT)
    first_popular_project_entry = Locator(By.CLASS_NAME, 'public-projects-item', settings.LONG_TIMEOUT)
    popular_projects = Locator(By.CSS_SELECTOR, '#osfHome > div.newAndNoteworthy > div > div:nth-child(2) > div > div > div:nth-child(1) > div:nth-child(2) > div > h4', settings.LONG_TIMEOUT)
    institutions_carousel_left_arrow = Locator(By.CSS_SELECTOR, '.left.carousel-control')
    institutions_carousel_right_arrow = Locator(By.CSS_SELECTOR, '.right.carousel-control')

    # Group locators
    institution_carousel_logos = GroupLocator(By.CLASS_NAME, 'img-circle')

    # Components
    create_project_modal = ComponentLocator(components.CreateProjectModal)
    project_created_modal = ComponentLocator(components.ProjectCreatedModal)
    project_list = ComponentLocator(components.ProjectList)
