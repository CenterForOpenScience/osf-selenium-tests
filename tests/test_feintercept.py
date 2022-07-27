import pytest
import settings
import requests
import os
import sys
import configparser
import js2py
from pages.files import FilesListPage
from pages.base import GuidBasePage
from pages.project import FilesPage, ProjectPage
from pages.search import SearchPage
from base.locators import ComponentLocator
from tests.test_dashboard import dashboard_page
from tests.test_my_projects import my_projects_page
from components.navbars import EmberNavbar, HomeNavbar, RegistriesNavbar
from api import osf_api
import markers  
import ipdb
import random
import threading as thread
import time
from selenium.webdriver.common.action_chains import ActionChains

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys

from pages.landing import LandingPage

from pages.login import (
    CASAuthorizationPage,
    GenericCASPage,
    InstitutionalLoginPage,
    LoginPage,
    Login2FAPage,
    LoginToSPage,
    login,
    LoginToSPage,
    InstitutionalLoginPage,
    GenericCASPage,
    login,
    login_admin,
    login_read_only,
    login_read_write,
    logout
)

from pages.dashboard import DashboardPage

from components.navbars import (
    HomeNavbar, 
    RegistriesNavbar
)

from pages.registries import (
    MyRegistrationsPage,
    RegistrationAddNewPage,
    RegistrationDetailPage,
    RegistrationDraftPage,
    RegistriesLandingPage,
    RegistriesDiscoverPage,
    RegistriesNavbar
)

from pages.preprints import (PreprintDiscoverPage)


@markers.core_functionality
class TestFEIntercept:
    # collect names using requirejs
    def test_collect_component_names(self, driver, user=osf_api.current_user()):
        url = 'https://staging2.osf.io/registries?view_only='
        login_read_write(driver)
 
        preprint_page = PreprintDiscoverPage(driver)
        preprint_page.goto()

        js_script = '''
        var documentObject = null;
        console.log("Preprint Page");
        if (documentObject == null || documentObject == undefined) { console.log("no context found"); }else{ documentObject = window.location.pathname; } console.log(documentObject);}
        console.log(requirejs.entries)
        '''
        driver.execute_script(js_script)

        ipdb.set_trace()

        assert True

        # logout(driver)
