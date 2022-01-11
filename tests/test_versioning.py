from base.locators import ComponentLocator
from tests.test_dashboard import dashboard_page
from tests.test_my_projects import my_projects_page
from api import osf_api
from components.navbars import EmberNavbar, HomeNavbar, RegistriesNavbar
import pytest
import markers
import settings
import requests
import os 
import sys
import configparser
import ipdb 
import random

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

# @pytest.fixture
# def user_contr_rw_login(driver):
#     login_page = LoginPage(driver)
#     login_page.goto()
#     return login_page

# @pytest.fixture
# def landing_page(driver):
#     landing_page = RegistriesLandingPage(driver)
#     landing_page.goto()
#     return landing_page

class TestVersioningElements:
    @markers.core_functionality
    def test_my_registries_upates_button_exists(self, driver, user = osf_api.current_user()):

        # login and go to dashboard
        login(driver)
        dashboard_page = DashboardPage(driver)
        dashboard_page.goto()
        DashboardPage(driver, verify=True)

        # find dropdown for registries and click it
        home_nav_bar = HomeNavbar(driver)
        home_dropdown_caret = home_nav_bar.service_dropdown
        home_dropdown_caret.click()
        home_registries_link = home_nav_bar.registries_link
        home_registries_link.click()

        # click add new registration button
        registries_navbar = RegistriesNavbar(driver)
        add_new_registration = registries_navbar.add_new_link
        add_new_registration.click()

        # verify on add new page
        registries_add_new_page = RegistrationAddNewPage(driver, verify=True)
        assert registries_add_new_page.dropdown_wormhole

        # add wait to ensure form loads (may be able to reduce wait later)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[data-test-new-registration-form]')
            )
        ) 

        # yes to projects 
        yes_button_exists = registries_add_new_page.has_project_button
        yes_button_exists.click()
        print("t:{}  v:{} ".format(type(yes_button_exists), yes_button_exists)) # print type and representation

        # NOTE uncomment for no projects and comment out yes logic
        # no_button_exists = registries_add_new_page.no_project_button
        # no_button_exists.click()

        project_power_select = registries_add_new_page.project_selection_dropdown
        project_power_select.click()

        # select first project
        # first_project = registries_add_new_page.first_project_selection
        # first_project.click()

        # select second project
        second_project = registries_add_new_page.second_project_selection
        second_project.click()

        WebDriverWait(driver, 5)

        # click registration schema type dropdown
        schema_power_select_dropdown = registries_add_new_page.schema_type_dropdown
        schema_power_select_dropdown.click()

        WebDriverWait(driver, 5)

        # select preregistration schema
        preregistration_schema_select = registries_add_new_page.preregistration_schema_selection
        preregistration_schema_select.click()

        WebDriverWait(driver, 5)

        ipdb.set_trace()
        # click submit 
        submit_button_add_new = registries_add_new_page.add_new_submit_button
        submit_button_add_new.click()

        # verify transition to draft page
        registration_draft_page = RegistrationDraftPage(driver, verify=True)
        draft_registration_page_identity = registration_draft_page.identity
        assert draft_registration_page_identity
        print("t:{}  v:{} ".format(type(draft_registration_page_identity), draft_registration_page_identity)) 

        # fill out title 
        input_registration_title = registration_draft_page.registration_title_input
        input_registration_title.clear()
        registration_random = str(random.randrange(1, 1000000))
        registration_title = 'Outcome Reporting Moderation Test'  + registration_random
        print(f'The Registration title is: ', registration_title)
        input_registration_title.send_keys(registration_title)

        WebDriverWait(driver, 5)

        # fill out description 
        input_registration_description = registration_draft_page.registration_description_input
        input_registration_description.clear()
        input_registration_description.send_keys('This registration is for testing the outcome reporting moderation workflow for versioning.')

        ipdb.set_trace()
        # click '+' add contributor button
        button_add_contributor = registration_draft_page.add_contributor_plus_button
        button_add_contributor.click()

        WebDriverWait(driver, 5)

        # clear contributor search box
        # TODO add logic for checking if contributors are present, ensure 1 admin is there
        search_box_add_contributor = registration_draft_page.add_contributor_search_box
        search_box_add_contributor.clear()

        # send keys for contributor name
        WebDriverWait(driver, 5)
        name = 'Ashley Robinson' # add to config later
        search_box_add_contributor.send_keys(name)

        # click search for contributor
        WebDriverWait(driver, 5)
        search_button_add_contributor = registration_draft_page.add_contributor_search_button
        search_button_add_contributor.click()

        # add first found contributor
        try: 
          result_add_first_contributor = registration_draft_page.add_first_contributor_result
          if(len(result_add_first_contributor) > 0):
            print(f'Contributor not yet added: ', s)
            result_add_first_contributor.click()
          else:
            print(f'Contributor already added')
              
        # except NoSuchElementException:
        except TypeError:
          print('There is a type mismatch')
        WebDriverWait(driver, 5)

        # click category dropdown 
        power_select_category = registration_draft_page.category_power_select
        power_select_category.click()

        WebDriverWait(driver, 5)

        # select analysis category
        dropdown_select_analysis_category = registration_draft_page.category_analysis_dropdown_select
        dropdown_select_analysis_category.click()

        WebDriverWait(driver, 5)

        # click license dropdown
        power_select_license = registration_draft_page.license_power_select
        power_select_license.click()

        WebDriverWait(driver, 5)

        # select cc international license
        select_license_cc_international = registration_draft_page.license_cc_international_select
        select_license_cc_international.click()

        WebDriverWait(driver, 5)

        # check engineering subject
        checkbox_engineering_subject = registration_draft_page.subject_engineering_checkbox
        isEngineeringChecked = checkbox_engineering_subject.is_selected()
        if isEngineeringChecked == False:
            checkbox_engineering_subject.click()

        WebDriverWait(driver, 5)

        # add tag for mirage moderation backend
        input_tags = registration_draft_page.tags_input
        input_tags.clear()
        input_tags.send_keys('cobalt')
        input_tags.send_keys(Keys.RETURN)

        WebDriverWait(driver, 5)

        ipdb.set_trace()
        # click next
        next_button_draft_registration = registration_draft_page.draft_registration_next_button
        next_button_draft_registration.click()

        # select for no data         
        # radio_button_no_data_collected = registration_draft_page.no_data_collected_radio_button
        # radio_button_no_data_collected.click()

        # select for data collected
        radio_button_data_collected = registration_draft_page.data_collected_radio_button
        radio_button_data_collected.click()

        WebDriverWait(driver, 5)

        # select for viewed data
        radio_button_data_looked_at = registration_draft_page.data_looked_at_radio_button
        radio_button_data_looked_at.click()

        WebDriverWait(driver, 10)

        # select for unviewed data
        # radio_button_data_not_looked_at = registration_draft_page.data_not_looked_at_radio_button
        # radio_button_data_not_looked_at.click()

        # TODO remove this trace
        ipdb.set_trace()

        # enter any additional comments
        textarea_comments = registration_draft_page.comments_textarea
        textarea_comments.clear()
        textarea_comments.send_keys('Thank you for attending this demo.')
        textarea_comments.send_keys(Keys.RETURN)

        # review entered answers
        review_button_draft = registration_draft_page.draft_review_button
        review_button_draft.click()

        WebDriverWait(driver, 5)

        # register draft
        register_button_draft = registration_draft_page.register_draft_button
        register_button_draft.click()

        # choose to make registration public 
        radio_make_registration_public = registration_draft_page.make_registration_public_radio
        radio_make_registration_public.click()

        # choose to make registration embargo 
        # add logic to get current time and add 5 years
        # radio_make_registration_embargo = registration_draft_page.make_registration_embargo_radio
        # register_button_draft.click()
        ipdb.set_trace()
        # cancel for demo purposes
        # back_button_demo = registration_draft_page.demo_back_button
        # back_button_demo.click()

        # register registration NOTE untested
        # register_button_draft = registration_draft_page.register_draft_button
        # register_button_draft.click()

        submit_button_draft = registration_draft_page.submit_draft_button
        submit_button_draft.click()
    
        ipdb.set_trace()
        logout(driver)


        