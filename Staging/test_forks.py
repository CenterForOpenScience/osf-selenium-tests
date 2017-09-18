'''
Created on Aug 22, 2017

@author: patrickanderson
'''
import settings
from blocks import login
from blocks import forks
from blocks import nodes

driver = settings.DRIVER


def test_forks():
    #l= Login()
    #n= Nodes()
    #f= Forks()
    login.login(driver)
    project_id = nodes.create_project(driver)
    fork_id = forks.create_fork_dashboard(driver)
    assert driver.find_element_by_id("nodeTitleEditable")
    nodes.delete_node(driver, fork_id + 'settings/')
    nodes.delete_node(driver, project_id + 'settings/')
    driver.quit()
