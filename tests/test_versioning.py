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
@markers.core_functionality
class TestVersioningElements:
        # login as read write user
        def test_handle_login_rw(self, driver, user=osf_api.current_user()):
            login_read_write(driver)
            print(f'Logging in as read write user')
            dashboard_page = DashboardPage(driver)
            dashboard_page.goto()
            DashboardPage(driver, verify=True)
            # logout(driver)

        # login as read only user
        def test_handle_login_ronly(self, driver, user=osf_api.current_user()):
            login_read_only(driver)
            print(f'Logging in as read only user')
            dashboard_page = DashboardPage(driver)
            dashboard_page.goto()
            DashboardPage(driver, verify=True)
            # logout(driver)

        # login as admin user
        def test_handle_login_rwx(self, driver, user=osf_api.current_user()):
            login_admin(driver)
            print(f'Logging in as admin user')
            dashboard_page = DashboardPage(driver)
            dashboard_page.goto()
            DashboardPage(driver, verify=True)
            # logout(driver)

        def test_handle_all_logout(self, driver, user=osf_api.current_user()):
            logout(driver)

        # find all contributor & email

        # navigate to gmail for each one

        # regex the title

        # click the approve button

        # close tab

        # do for each in array of conributor emails

        # create a edit

        # approve by the same approve email but for edits

        # rename a file
        def test_files_page_redesign(self, driver, user = osf_api.current_user()):
            TestVersioningElements.test_handle_login_rwx(self, driver, user = osf_api.current_user())

            # login(driver)
            dashboard_page = DashboardPage(driver)
            ac = ActionChains(driver)
            dashboard_page.goto()
            DashboardPage(driver, verify=True)

            collect_name = 'console.log(requirejs.entries);'

            driver.execute_script(collect_name)

            ipdb.set_trace()

            # find search bar and search Registries
            search_page = SearchPage(driver) #not search page, update
            search_bar = search_page.search_bar # search bar locator is correct, transport
            search_bar.click()
            project_name = 'African and European Birbs' # TODO place in Excel
            search_bar.send_keys(project_name)
            WebDriverWait(driver, 5)
            search_bar.send_keys(Keys.ENTER)
            WebDriverWait(driver, 5)

            ipdb.set_trace()
            first_matching_result = dashboard_page.result_first_match
            print(first_matching_result)
            first_matching_result.click()

            project_page = ProjectPage(driver)

            project_page_title = project_page.title

            project_inner_html = project_page_title.get_property("innerHTML").strip()

            print("{}".format(project_inner_html))
            string_project_title = "{}".format(project_inner_html)
            if string_project_title == project_name:
                print('Project names match, proceeding with test')
            else:
                print('Config project name and title do not match')
            # print( project_page_title.__str__)
            # assert project_page_title == project_name

            # click file on file widget
            # file_provider = project_page.file_widget
            # print("v:{} ".format(type(file_provider), file_provider))
            # print(file_provider)

            # click Registrations tab

            project_files_tab = project_page.project_files_tab
            # add logic for window sizing
            project_files_tab.click()
            WebDriverWait(driver, 5)

            files_list_view = FilesListPage(driver)
            current_url = driver.current_url
            files_list_url = files_list_view.url
            # files_list_view = files_page

            print("{}".format(current_url))
            print("{}".format(files_list_url))

            # select provider
            provider = 'osfstorage' # TODO place in Excel


            # redirect to file detail
            first_file = files_list_view.file_link
            print(f'The current page:', driver.title)


            # ActionChains(mydriver).key_up(Keys.ALT).perform()

            first_file.click()
            # ac.move_to_element(first_file).key_down(Keys.ALT).click().key_up(Keys.ALT).perform()
            ac.key_down(Keys.COMMAND).key_down('W').perform()
            ipdb.set_trace()
            # first_file.send_keys(Keys.COMMAND)
            # first_file.send_keys('W')

            file_list_tab = driver.window_handles[0]
            #obtain browser tab window
            file_detail_tab  = driver.window_handles[1]
            driver.switch_to.window(file_detail_tab)
            print(f'The current page:', driver.title)
            driver.close()
            print(f'The current page:', driver.title)


            # select file action
            file_actions_menu =  files_list_view.file_actions_menu
            file_actions_menu.click()


            # download file click
            download_file = files_list_view.download_file_action
            download_file.click()

            # delete file
            delete_file = files_list_view.delete_file_action
            delete_file.click()
                # cancel delete
                # delete delete

            #  embed file
                # JS
                # HTML
            # share
                # email
                # FB
                # Twitter

                

            ipdb.set_trace()

            # Files from Registrations

            # ensure card title is the same as above ^

            # registration_card =

            # registration_card_title =

            # click first matching card title

            # click storage provider

            # Click Files

            # click first file

            # return only osfstorage or EGAP by clicking text box
            # find if Registration contains a file
            # if so, click Registration

            # click Files tab

            # def navigate_to_dashboard():

            # def rename_file():

            # def rename_folder():



        # create registration
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
                    print(f'Contributor not yet added: ')
                    result_add_first_contributor.click()
                else:
                    print(f'Contributor already added')
            # except NoSuchElementException:
            except TypeError:
                print(f'There is a type mismatch')
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

        def runAllVersioning(self):
            if __name__ == '__main__':
                thread.Thread(target = self.handle_login).start()
                thread.Thread(target = self.test_my_registries_upates_button_exists).start()


    # run = TestVersioningElements()
    # run.runAllVersioning()
        