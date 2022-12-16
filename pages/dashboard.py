from selenium.webdriver.common.by import By

import components.dashboard as components
import settings
from base.locators import (
    ComponentLocator,
    GroupLocator,
    Locator,
)
from components.navbars import EmberNavbar
from pages.base import OSFBasePage


class BaseDashboardPage(OSFBasePage):
    def get_institutions(self):
        page_institutions = self.institution_carousel_logos
        while self.institutions_carousel_left_arrow.present():
            self.institutions_carousel_right_arrow.click()
            for logo in self.institution_carousel_logos:
                if logo in page_institutions:
                    return page_institutions
                page_institutions.append(logo)
            return page_institutions
        return []


class DashboardPage(BaseDashboardPage):
    url = settings.OSF_HOME + '/dashboard/'

    identity = Locator(
        By.CSS_SELECTOR, '._institutions-panel_1b28t4', settings.LONG_TIMEOUT
    )
    create_project_button = Locator(
        By.CSS_SELECTOR,
        '[data-test-create-project-modal-button]',
        settings.LONG_TIMEOUT,
    )
    view_meetings_button = Locator(By.XPATH, '//a[text()="View meetings"]')
    view_preprints_button = Locator(By.XPATH, '//a[text()="View preprints"]')
    first_noteworthy_project = Locator(
        By.CSS_SELECTOR, '[data-test-noteworthy-project]', settings.LONG_TIMEOUT
    )
    institutions_carousel_left_arrow = Locator(
        By.CSS_SELECTOR, '.carousel-control.left'
    )
    institutions_carousel_right_arrow = Locator(
        By.CSS_SELECTOR, '.carousel-control.right'
    )

    # Group Locators
    institution_carousel_logos = GroupLocator(By.CSS_SELECTOR, '.carousel-inner img')

    # Components
    navbar = ComponentLocator(EmberNavbar)
    create_project_modal = ComponentLocator(components.EmberCreateProjectModal)
    project_created_modal = ComponentLocator(components.EmberProjectCreatedModal)
    project_list = ComponentLocator(components.EmberProjectList, settings.LONG_TIMEOUT)
