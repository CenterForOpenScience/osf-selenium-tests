from blocks.variables import Variables
from blocks.search import Search

driver = Variables.driver

def test_search():
	s = Search()
	s.staging_nav_bar(driver)
	driver.quit()
