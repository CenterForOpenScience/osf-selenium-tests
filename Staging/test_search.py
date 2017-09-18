import settings
from blocks import search

driver = settings.DRIVER

def test_search():
	# s = Search()
	search.staging_navbar(driver)
	search.staging_search_navbar(driver)
	search.staging_bottom_bar(driver)
	driver.quit()
