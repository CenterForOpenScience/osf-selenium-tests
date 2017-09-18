import settings
from blocks import login
from blocks import forks
from blocks import nodes
from blocks import contributors

driver = settings.DRIVER

def test_contributors():
    login.login(driver)
    project_id = nodes.create_project(driver)
    contributors.search_add_contributor(driver)
    contributors.changetoread_contributor(driver)
    contributors.reorder_contributor(driver)
    nodes.delete_node(driver, project_id + 'settings/')
    driver.quit()