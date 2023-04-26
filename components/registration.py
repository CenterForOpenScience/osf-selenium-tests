from selenium.webdriver.common.by import By

from base.locators import (
    BaseElement,
    Locator,
)


class SubmittedSideNavbar(BaseElement):
    """This is the side navigation bar for a submitted registration"""

    overview_link = Locator(By.CSS_SELECTOR, 'a[data-analytics-name="Overview"]')
    metadata_link = Locator(By.CSS_SELECTOR, 'a[data-analytics-name="Metadata"]')
    files_link = Locator(By.CSS_SELECTOR, 'a[data-analytics-name="Files"]')
    resources_link = Locator(By.CSS_SELECTOR, 'a[data-analytics-name="Resources"]')
    wiki_link = Locator(By.CSS_SELECTOR, 'a[data-analytics-name="Wiki"]')
    components_link = Locator(By.CSS_SELECTOR, 'a[data-analytics-name="Components"]')
    links_link = Locator(By.CSS_SELECTOR, 'a[data-analytics-name="Links"]')
    analytics_link = Locator(By.CSS_SELECTOR, 'a[data-analytics-name="Analytics"]')
    comments_link = Locator(By.CSS_SELECTOR, 'a[data-analytics-name="Comments"]')
