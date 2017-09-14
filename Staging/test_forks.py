'''
Created on Aug 22, 2017

@author: patrickanderson
'''
from blocks.login import Login
from blocks.forks import Forks
from blocks.nodes import Nodes
from blocks.variables import Variables

driver = Variables.driver


def test_forks():
    login.Login(driver)
    project_id = Nodes.create_project(driver)
    fork_id = Forks.create_fork_dashboard(driver)
    assert driver.find_element_by_id("nodeTitleEditable")
    Nodes.delete_node(driver, fork_id + 'settings/')
    Nodes.delete_node(driver, project_id + 'settings/')
    driver.quit()
