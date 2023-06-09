import re

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import markers
import settings
from api import osf_api
from pages.login import (
    LoginPage,
    login,
    logout,
)
from pages.project import (
    ForksPage,
    ProjectPage,
    RequestAccessPage,
)


@pytest.fixture()
def project_page(driver, default_project_page):
    default_project_page.goto()
    return default_project_page


@pytest.fixture()
def project_page_with_file(driver, project_with_file):
    project_page = ProjectPage(driver, guid=project_with_file.id)
    project_page.goto()
    return project_page


@pytest.mark.usefixtures('must_be_logged_in')
class TestProjectDetailPage:
    @markers.smoke_test
    @markers.core_functionality
    def test_change_title(self, project_page, fake):

        new_title = fake.sentence(nb_words=4)
        assert project_page.title.text != new_title
        # In some cases (especially with Chrome) the test steps are executed faster than the web page is
        # really ready for them.  In this particular case the test clicks the title of the project which
        # is supposed to then produce an input box in which you can change the title.  If the click is
        # performed before the page is ready, then there is no input box and the test fails.  So we need
        # to provide a little extra time.  We can do this by waiting on the log widget to load.
        project_page.log_widget.loading_indicator.here_then_gone()
        project_page.title.click()
        project_page.title_input.clear()
        project_page.title_input.send_keys(new_title)
        project_page.title_edit_submit_button.click()
        project_page.verify()  # Wait for the page to reload
        assert project_page.title.text == new_title

    @markers.smoke_test
    @markers.core_functionality
    def test_log_widget_loads(self, project_page):
        project_page.log_widget.loading_indicator.here_then_gone()
        assert project_page.log_widget.log_items

    @markers.dont_run_on_prod
    @markers.dont_run_on_preferred_node
    @markers.core_functionality
    def test_make_public(self, driver, project_page):
        # Set project to public
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(), "Make Public")]')
            )
        )
        project_page.make_public_link.click()

        # First click the Cancel link on the Confirm Modal and verify that the project
        # is still private.
        project_page.confirm_privacy_change_modal.cancel_link.click()
        assert project_page.make_private_link.absent()

        # Click the Make Public link again and this time click the Confirm link on the
        # modal to actually make the project public.
        project_page.make_public_link.click()
        project_page.confirm_privacy_change_modal.confirm_link.click()
        assert project_page.make_private_link.present()

        # Confirm logged out user can now see project
        logout(driver)
        project_page.goto()
        assert ProjectPage(driver, verify=True)
        login(driver)

    @markers.smoke_test
    @markers.core_functionality
    def test_file_widget_loads(self, project_page_with_file):
        # Check the uploaded file shows up in the files widget
        project_page_with_file.file_widget.loading_indicator.here_then_gone()
        assert project_page_with_file.file_widget.first_file

    @markers.smoke_test
    @pytest.mark.skipif(
        not settings.PREFERRED_NODE,
        reason='Only run this test if addons are set up on a specific node.',
    )
    def test_addon_files_load(self, project_page, session, driver):
        """This test is very fragile and makes assumptions about your setup.
        You must have all of the addons in `EXPECTED_PROVIDERS` connected to your `PREFERRED_NODE`.
        In each provider you must have a file named `<provider_name>.txt`.

        The test will fail if you do not have the expected providers connected.
        The test will also fail if you have not named your files correctly.
        """
        providers = osf_api.get_node_addons(session, project_page.guid)
        assert set(providers) == set(settings.EXPECTED_PROVIDERS)
        project_page.file_widget.loading_indicator.here_then_gone()
        project_page.file_widget.file_expander.here_then_gone()
        project_page.file_widget.filter_button.click()
        for provider in providers:
            project_page.file_widget.filter_input.clear()
            project_page.file_widget.filter_input.send_keys_deliberately(provider)
            driver.find_element_by_xpath(
                "//*[contains(text(), '{}')]".format(provider + '.txt')
            )


@pytest.mark.usefixtures('must_be_logged_in_as_user_two')
class TestProjectDetailAsNonContributor:
    @markers.smoke_test
    @markers.core_functionality
    def test_is_private(self, driver, default_project_page):
        # Verify that a non contributor on a private project gets the request access page
        default_project_page.goto(expect_redirect_to=RequestAccessPage)


class TestProjectDetailLoggedOut:
    @markers.smoke_test
    @markers.core_functionality
    def test_is_private(self, driver, default_project_page):
        # Verify that a logged out user cannot see the project
        default_project_page.goto(expect_redirect_to=LoginPage)


class TestForksPage:
    @pytest.fixture()
    def forks_page(self, driver, default_project):
        forks_page = ForksPage(driver, guid=default_project.id)
        forks_page.goto()
        return forks_page

    @markers.dont_run_on_prod
    @markers.core_functionality
    def test_create_fork(self, driver, session, must_be_logged_in, forks_page):
        forks_page.placeholder_text.present()
        assert len(forks_page.listed_forks) == 0
        forks_page.new_fork_button.click()
        forks_page.create_fork_modal_button.click()
        forks_page.info_toast.present()
        forks_page.reload()
        forks_page.verify()
        forks_page.fork_authors.present()
        assert len(forks_page.listed_forks) == 1

        # Clean-up leftover fork
        fork_guid = forks_page.fork_link.get_attribute('data-test-node-title')
        osf_api.delete_project(session, fork_guid, None)


@markers.dont_run_on_prod
@pytest.mark.usefixtures('must_be_logged_in')
class TestProjectComponents:
    def test_add_component(self, driver, session, project_page):
        """Test the functionality of adding a new child component node to a project"""

        # Click Add Component button and on the Create Component Modal, first click the
        # Cancel button and verify that there are no components listed on the Project
        # Overview page.
        project_page.loading_indicator.here_then_gone()
        project_page.add_component_button.click()
        project_page.create_component_modal.cancel_button.click()
        WebDriverWait(driver, 3).until(
            EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, 'div.modal-backdrop.fade')
            )
        )
        assert len(project_page.components) == 0

        # Click the Add Component button again and this time enter data on the modal to
        # add a new component
        project_page.add_component_button.click()
        project_page.create_component_modal.title_input.click()
        project_page.create_component_modal.title_input.send_keys_deliberately(
            'Selenium Component'
        )
        project_page.create_component_modal.more_link.click()
        project_page.create_component_modal.description_input.click()
        project_page.create_component_modal.description_input.send_keys_deliberately(
            'This component was added by an automated selenium test.'
        )
        project_page.scroll_into_view(
            project_page.create_component_modal.create_component_button.element
        )
        project_page.create_component_modal.create_component_button.click()

        # Get the guid for the component from the Go to new component link on the
        # Component Created Confirmation modal
        match = re.search(
            r'([a-z0-9]{4,8})\.osf\.io/([a-z0-9]{5})',
            project_page.component_created_modal.go_to_new_component_link.get_attribute(
                'href'
            ),
        )
        component_guid = match.group(2)

        try:
            # Click the Go to new component link and verify that you are navigated to
            # the Overview page of a new node
            project_page.component_created_modal.go_to_new_component_link.click()
            component_page = ProjectPage(driver, verify=True)
            assert component_page.title.text == 'Selenium Component'
            assert (
                component_page.description.text
                == 'This component was added by an automated selenium test.'
            )

            # Click the link to the parent project at the top of the page to navigate
            # back to the original parent Project Overview page.
            component_page.parent_project_link.click()
            assert project_page

            # Verify that the Components section of the parent Project now lists the
            # new component
            assert len(project_page.components) == 1
            component = project_page.get_component_by_node_id(component_guid)
            assert (
                component.find_element_by_css_selector('div > h4 > span > a').text
                == 'Selenium Component'
            )
        finally:
            # The parent project should be automatically deleted by the fixture code.
            # But it cannot be deleted if the component is not deleted first.
            osf_api.delete_project(session, component_guid, None)

    def test_delete_component_from_project(self, driver, session, default_project):
        """Test the functionality of deleting a child component node from the parent
        project's Project Overview page.
        """

        # First use the api to create a child node for the dummy temporary project
        component = osf_api.create_child_node(
            session, node=default_project, title='API Created Component'
        )

        try:
            # Navigate to the parent Project Overview page and verify the existence of
            # the component
            project_page = ProjectPage(driver, guid=default_project.id)
            project_page.goto()
            assert ProjectPage(driver, verify=True)
            assert len(project_page.components) == 1
            component_card = project_page.get_component_by_node_id(component.id)
            assert (
                component_card.find_element_by_css_selector('div > h4 > span > a').text
                == 'API Created Component'
            )

            # Click the button on the right side of the component card to reveal a
            # dropdown options menu
            component_card.find_element_by_css_selector(
                'div > h4 > div > div > button'
            ).click()

            # Click the Delete menu option
            component_card.find_element_by_css_selector(
                'div > h4 > div > div > ul > li:nth-child(3) > a'
            ).click()

            # On the Delete Component Confirmation Modal, first verify that the Delete
            # button is disabled. Then click the Cancel button to go back to the Project
            # Overview page again and verify the component card is still there.
            WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, 'nodesDelete'))
            )
            assert driver.find_element(
                By.CSS_SELECTOR,
                '#nodesDelete > div > div > div > div.modal-footer > span:nth-child(3) > a.btn.btn-danger.disabled',
            )
            project_page.delete_component_modal.cancel_link.click()
            WebDriverWait(driver, 3).until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, 'div.modal-backdrop.fade')
                )
            )
            assert len(project_page.components) == 1

            # Select the Component Delete menu option again and this time enter the
            # confirmation text value in the input field and click the Delete button to
            # actually delete the component.
            component_card.find_element_by_css_selector(
                'div > h4 > div > div > button'
            ).click()
            component_card.find_element_by_css_selector(
                'div > h4 > div > div > ul > li:nth-child(3) > a'
            ).click()
            WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, 'nodesDelete'))
            )
            project_page.delete_component_modal.confirmation_input.send_keys_deliberately(
                project_page.delete_component_modal.confirmation_text.text
            )
            WebDriverWait(driver, 3).until(
                EC.invisibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        '#nodesDelete > div > div > div > div.modal-footer > span:nth-child(3) > a.btn.btn-danger.disabled',
                    )
                )
            )
            project_page.delete_component_modal.delete_link.click()

            # Verify that back on the Project Overview page an alert message appears at
            # the top of the page indicating that the component was deleted and the
            # Component section no longer has the card for the deleted component.
            WebDriverWait(driver, 5).until(
                EC.visibility_of(project_page.alert_message.element)
            )
            assert (
                project_page.alert_message.text
                == 'Component has been successfully deleted.'
            )
            assert len(project_page.components) == 0
        finally:
            # We must make sure that in the event of an error that we delete the
            # component so that the dummy project can also be deleted.
            if osf_api.get_node(session, node_id=component.id):
                osf_api.delete_project(session, component.id, None)

    def test_make_public_project_with_component(self, driver, session, default_project):
        """Test the functionality of making Public a project that has a child component
        node.
        """

        # First use the api to create a child node for the dummy temporary project
        component = osf_api.create_child_node(
            session, node=default_project, title='API Created Component'
        )

        try:
            # Navigate to the parent Project Overview page and verify the existence of
            # the component
            project_page = ProjectPage(driver, guid=default_project.id)
            project_page.goto()
            assert ProjectPage(driver, verify=True)
            assert len(project_page.components) == 1
            component_card = project_page.get_component_by_node_id(component.id)
            assert (
                component_card.find_element_by_css_selector('div > h4 > span > a').text
                == 'API Created Component'
            )

            # Click the Make Public link at the top of the page and then click the
            # Continue link on the first confirmation modal.
            project_page.make_public_link.click()
            project_page.confirm_privacy_change_modal.continue_link.click()

            # On the Change privacy settings for components modal, first click the
            # Cancel link and verify you are back on the Project Overview page and
            # the project is still private.
            project_page.components_privacy_change_modal.cancel_link.click()
            assert project_page.make_public_link.present()

            # Click the Make Public link again and this time follow through with
            # making the project public.
            project_page.make_public_link.click()
            project_page.confirm_privacy_change_modal.continue_link.click()

            # Back on the Change privacy settings for components modal, click the
            # checkbox for the component and then click the Continue link.
            project_page.components_privacy_change_modal.first_component_checkbox.click()
            project_page.components_privacy_change_modal.continue_link.click()

            # Click the Confirm link on the final modal
            project_page.confirm_privacy_change_modal.confirm_link.click()
            assert project_page.make_private_link.present()

            # Verify logged out user can now see project
            logout(driver)
            project_page.goto()
            assert ProjectPage(driver, verify=True)

            # Also navigate to Component and verify logged out user can see it as well
            component_page = ProjectPage(driver, guid=component.id)
            component_page.goto()
            assert ProjectPage(driver, verify=True)
        finally:
            # We must make sure that in the event of an error that we delete the
            # component so that the dummy project can also be deleted.
            if osf_api.get_node(session, node_id=component.id):
                osf_api.delete_project(session, component.id, None)


@markers.dont_run_on_prod
@pytest.mark.usefixtures('hide_footer_slide_in')
class TestProjectVOLs:
    def test_vol_project_overview_page(self, driver, session, project_with_file):
        """Test that creates a View Only Link using the OSF api and then uses that VOL
        to navigate to the Project Overview page for the project.
        """

        vol_key = osf_api.create_project_view_only_link(session, project_with_file.id)
        # Create the VOL URL for the Project and use the link to navigate to the Project
        # Overview page
        vol_url = (
            settings.OSF_HOME + '/' + project_with_file.id + '/?view_only=' + vol_key
        )
        driver.get(vol_url)
        project_page = ProjectPage(driver, verify=True)
        project_page.loading_indicator.here_then_gone()

        # Verify that we are not logged in
        assert project_page.is_logged_out()

        # Verify VOL message at the top of the page
        assert (
            project_page.alert_info_message.text
            == 'This project is being viewed through a private, view-only link. Anyone with the link can view this project. Keep the link safe.'
        )

        # Verify Contributor is visible
        user = osf_api.current_user()
        assert project_page.contributors_list.text == user.full_name

        # Verify File Widget loads
        assert project_page.file_widget.first_file

        # Verify Log Widget loads
        assert project_page.log_widget.log_items

    def test_avol_project_overview_page(self, driver, session, project_with_file):
        """Test that creates an Anonymous View Only Link using the OSF api and then uses
        that AVOL to navigate to the Project Overview page for the project.
        """

        avol_key = osf_api.create_project_view_only_link(
            session, project_with_file.id, anonymous=True
        )
        # Create the AVOL URL for the Project and use the link to navigate to the Project
        # Overview page
        avol_url = (
            settings.OSF_HOME + '/' + project_with_file.id + '/?view_only=' + avol_key
        )
        driver.get(avol_url)
        project_page = ProjectPage(driver, verify=True)
        project_page.loading_indicator.here_then_gone()

        # Verify that we are not logged in
        assert project_page.is_logged_out()

        # Verify VOL message at the top of the page
        assert (
            project_page.alert_info_message.text
            == 'This project is being viewed through a private, view-only link. Anyone with the link can view this project. Keep the link safe.'
        )

        # Verify Contributor is NOT visible
        assert project_page.contributors_list.text == 'Anonymous Contributors'

        # Verify File Widget loads
        assert project_page.file_widget.first_file

        # Verify Log Widget loads
        assert project_page.log_widget.log_items
