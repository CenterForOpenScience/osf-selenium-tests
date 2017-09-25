import settings
from helpers import search

driver = settings.DRIVER

def test_search():
	search.staging_navbar(driver)
	search.staging_search_navbar(driver)
	search.staging_bottom_bar(driver)
	driver.quit()
