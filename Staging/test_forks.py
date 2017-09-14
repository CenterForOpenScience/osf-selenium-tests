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
    l= Login()
    n= Nodes()
    f= Forks()
    l.staging_login(driver)
    project_id = n.create_project(driver)
    fork_id = f.create_fork_dashboard(driver)
    assert driver.find_element_by_id("nodeTitleEditable")
    n.delete_node(driver, fork_id + 'settings/')
    n.delete_node(driver, project_id + 'settings/')
    driver.quit()
