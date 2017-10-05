#import settings
import os
from helpers import login
from helpers import forks
from helpers import nodes
from helpers import contributors

#driver = DRIVER
shikha = os.environ['shikha']
#DRIVER= webdriver.Remote(command_executor, desired_capabilities=DESIRED_CAP)

def test_contributors():
    print(shikha)
    login.login(DRIVER)
    project_id = nodes.create_project(driver)
    contributors.search_add_contributor(driver)
    contributors.changetoread_contributor(driver)
    contributors.reorder_contributor(driver)
    nodes.delete_node(driver, project_id + 'settings/')
    driver.quit()
