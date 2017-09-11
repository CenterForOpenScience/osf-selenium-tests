from selenium import webdriver
from blocks.login import Login
from blocks.forks import Forks
from blocks.nodes import Nodes
from blocks.contributors import Contributors

desired_cap = {'browser': 'Chrome', 'browser_version': '60.0', 'os': 'Windows', 'os_version': '10', 'resolution': '2048x1536'}
driver = webdriver.Remote(
command_executor='http://osfselenium1:9asHrZGoyk7Tesx9agX5@hub.browserstack.com:80/wd/hub',
desired_capabilities=desired_cap)

def test_contributors():
    l = Login()
    p = Nodes()
    c= Contributors()
    Login.login(driver)
    project_id = Nodes.create_project(driver)
    Contributors.search_add_contributor(driver)
    Contributors.changetoread_contributor(driver)
    Contributors.reorder_contributor(driver)
    Nodes.delete_node(driver, project_id + 'settings/')
    driver.quit()
