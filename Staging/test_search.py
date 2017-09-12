from blocks.variables import Variables
from blocks.search import Search

driver = Variables.driver

def test_search():
	s = Search()
	s.staging_navbar(driver)
	driver.quit()
