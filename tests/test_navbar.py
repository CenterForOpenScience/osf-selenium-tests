import pytest

import markers
from api import osf_api
from pages.cos import COSDonatePage
from pages.dashboard import DashboardPage
from pages.institutions import InstitutionsLandingPage
from pages.landing import LandingPage
from pages.login import LoginPage
from pages.meetings import MeetingsPage
from pages.preprints import (
    PreprintDiscoverPage,
    PreprintLandingPage,
    PreprintSubmitPage,
    ReviewsDashboardPage,
)
from pages.project import MyProjectsPage, ProjectPage
from pages.register import RegisterPage
from pages.registrations import MyRegistrationsPage
from pages.registries import (
    RegistrationAddNewPage,
    RegistriesLandingPage,
)
from pages.collections import CollectionDiscoverPage, CollectionSubmitPage
from pages.search import SearchPage
from pages.support import SupportPage
from pages.user import (
    ProfileInformationPage,
    UserProfilePage,
)


class NavbarTestLoggedOutMixin:
    """Mixin used to inject generic tests"""

    @pytest.fixture()
    def page(self, driver):
        raise NotImplementedError()

    def test_osf_home_dropdown_link(self, page, driver):
        page.navbar.service_dropdown.click()
        page.navbar.home_link.click()
        LandingPage(driver, verify=True)

    def test_preprints_dropdown_link(self, page, driver):
        page.navbar.service_dropdown.click()
        page.navbar.preprints_link.click()
        PreprintLandingPage(driver, verify=True)

    def test_registries_dropdown_link(self, driver, page):
        page.navbar.service_dropdown.click()
        page.navbar.registries_link.click()
        RegistriesLandingPage(driver, verify=True)

    def test_meetings_dropdown_link(self, page, driver):
        page.navbar.service_dropdown.click()
        page.navbar.meetings_link.click()
        MeetingsPage(driver, verify=True)

    def test_institutions_dropdown_link(self, page, driver):
        page.navbar.service_dropdown.click()
        page.navbar.institutions_link.click()
        InstitutionsLandingPage(driver, verify=True)

    def test_donate_link(self, page, driver):
        page.navbar.donate_link.click()
        donate_page = COSDonatePage(driver, verify=False)
        assert_donate_page(driver, donate_page)

    def test_sign_in_button(self, page, driver):
        page.navbar.sign_in_button.click()
        LoginPage(driver, verify=True)

    def test_sign_up_button(self, driver, page):
        page.navbar.sign_up_button.click()
        RegisterPage(driver, verify=True)

    def test_user_dropdown_not_present(self, page):
        assert page.navbar.user_dropdown.absent()


class NavbarTestLoggedInMixin:
    """Mixin used to inject generic tests"""

    @pytest.fixture()
    def page(self, driver):
        raise NotImplementedError()

    def test_user_profile_menu_profile_link(self, driver, page):
        page.navbar.user_dropdown.click()
        page.navbar.user_dropdown_profile.click()
        assert UserProfilePage(driver, verify=True)

    def test_user_profile_menu_support_link(self, driver, page):
        page.navbar.user_dropdown.click()
        page.navbar.user_dropdown_support.click()
        assert SupportPage(driver, verify=True)

    def test_user_profile_menu_settings_link(self, driver, page):
        page.navbar.user_dropdown.click()
        page.navbar.user_dropdown_settings.click()
        assert ProfileInformationPage(driver, verify=True)

    def test_sign_in_button_not_present(self, page):
        assert page.navbar.sign_in_button.absent()

    def test_sign_up_button_not_present(self, page):
        assert page.navbar.sign_up_button.absent()

    def test_logout_link(self, driver, page):
        page.navbar.user_dropdown.click()
        page.navbar.logout_link.click()
        LandingPage(driver, verify=True)


@markers.smoke_test
@markers.core_functionality
class TestOSFHomeNavbarLoggedOut(NavbarTestLoggedOutMixin):
    @pytest.fixture()
    def page(self, driver):
        page = LandingPage(driver)
        page.goto_with_reload()
        return page

    def test_my_projects_link_not_present(self, page):
        assert page.navbar.my_projects_link.absent()

    def test_search_link(self, driver, page):
        page.navbar.search_link.click()
        assert SearchPage(driver, verify=True)

    def test_support_link(self, page, driver):
        page.navbar.support_link.click()
        assert SupportPage(driver, verify=True)


@markers.smoke_test
@markers.core_functionality
class TestOSFHomeNavbarLoggedIn(NavbarTestLoggedInMixin):
    @pytest.fixture()
    def page(self, driver, log_in_if_not_already):
        page = DashboardPage(driver)
        page.goto_with_reload()
        return page

    def test_my_projects_link(self, page, driver):
        page.navbar.my_projects_link.click()
        assert MyProjectsPage(driver, verify=True)


@markers.smoke_test
@markers.core_functionality
class TestPreprintsNavbarLoggedOut(NavbarTestLoggedOutMixin):
    @pytest.fixture()
    def page(self, driver):
        page = PreprintLandingPage(driver)
        page.goto_with_reload()
        return page

    def test_search_link(self, page, driver):
        page.navbar.search_link.click()
        PreprintDiscoverPage(driver, verify=True)

    def test_support_link(self, page, driver):
        page.navbar.support_link.click()
        assert SupportPage(driver, verify=True)

    def test_sign_up_button(self, page, driver):
        page.navbar.sign_up_button.click()
        # Sign Up button takes you to a more specific OSF Preprints sign up page
        assert 'campaign' and 'preprints' in driver.current_url


@markers.smoke_test
@markers.core_functionality
@pytest.mark.usefixtures('log_in_if_not_already')
class TestPreprintsNavbarLoggedIn(NavbarTestLoggedInMixin):
    @pytest.fixture()
    def page(self, driver):
        page = PreprintLandingPage(driver)
        page.goto_with_reload()
        return page

    def test_add_a_preprint_link(self, page, driver):
        page.navbar.add_a_preprint_link.click()
        PreprintSubmitPage(driver, verify=True)

    def test_my_preprints_link(self, page, driver):
        page.navbar.my_preprints_link.click()
        # My Preprints link actually navigates to My Preprints section of My Projects page
        assert 'myprojects/#preprints' in driver.current_url

    # In order to see the My Reviewing link in the Preprints Navbar the user has to be
    # an admin for one of the Branded Preprint Providers.
    @markers.dont_run_on_prod
    def test_my_reviewing_link(self, page, driver):
        page.navbar.my_reviewing_link.click()
        ReviewsDashboardPage(driver, verify=True)


@markers.smoke_test
@markers.core_functionality
class TestRegistriesNavbarLoggedOut(NavbarTestLoggedOutMixin):
    @pytest.fixture()
    def page(self, driver):
        page = RegistriesLandingPage(driver)
        page.goto_with_reload()
        return page

    def test_help_link(self, page, driver):
        page.navbar.help_link.click()
        assert SupportPage(driver, verify=True)

    # In the Registries navbar there is no Sign Up button, instead it is a Join link
    def test_sign_up_button(self, page, driver):
        page.navbar.join_link.click()
        # Join link takes you to a more specific OSF Registries sign up page
        assert 'campaign=osf-registries' in driver.current_url

    # In the Registries navbar there is no Sign In button, instead it is a Login link
    def test_sign_in_button(self, page, driver):
        page.navbar.login_link.click()
        LoginPage(driver, verify=True)


@markers.smoke_test
@markers.core_functionality
@pytest.mark.usefixtures('log_in_if_not_already')
class TestRegistriesNavbarLoggedIn(NavbarTestLoggedInMixin):
    @pytest.fixture()
    def page(self, driver):
        page = RegistriesLandingPage(driver)
        page.goto_with_reload()
        return page

    def test_add_new_link(self, page, driver):
        page.navbar.add_new_link.click()
        RegistrationAddNewPage(driver, verify=True)

    def test_my_registrations_link(self, page, driver):
        page.navbar.my_registrations_link.click()
        MyRegistrationsPage(driver, verify=True)


@markers.smoke_test
@markers.core_functionality
class TestMeetingsNavbarLoggedOut(NavbarTestLoggedOutMixin):
    @pytest.fixture()
    def page(self, driver):
        page = MeetingsPage(driver)
        page.goto_with_reload()
        return page

    def test_search_link(self, driver, page):
        page.navbar.search_link.click()
        SearchPage(driver, verify=True)

    def test_support_link(self, page, driver):
        page.navbar.support_link.click()
        assert SupportPage(driver, verify=True)


@markers.smoke_test
@markers.core_functionality
@pytest.mark.usefixtures('log_in_if_not_already')
class TestMeetingsNavbarLoggedIn(NavbarTestLoggedInMixin):
    @pytest.fixture()
    def page(self, driver):
        page = MeetingsPage(driver)
        page.goto_with_reload()
        return page

    def test_my_projects_link(self, page, driver):
        page.navbar.my_projects_link.click()
        assert MyProjectsPage(driver, verify=True)


@markers.smoke_test
@markers.core_functionality
class TestInstitutionsNavbarLoggedOut(NavbarTestLoggedOutMixin):
    @pytest.fixture()
    def page(self, driver):
        page = InstitutionsLandingPage(driver)
        page.goto_with_reload()
        return page

    def test_search_link(self, driver, page):
        page.navbar.search_link.click()
        SearchPage(driver, verify=True)

    def test_support_link(self, page, driver):
        page.navbar.support_link.click()
        SupportPage(driver, verify=True)


@markers.smoke_test
@markers.core_functionality
@pytest.mark.usefixtures('log_in_if_not_already')
class TestInstitutionsNavbarLoggedIn(NavbarTestLoggedInMixin):
    @pytest.fixture()
    def page(self, driver):
        page = InstitutionsLandingPage(driver)
        page.goto_with_reload()
        return page

    def test_my_projects_link(self, page, driver):
        page.navbar.my_projects_link.click()
        assert MyProjectsPage(driver, verify=True)


def assert_donate_page(driver, donate_page):
    # locators.py does not currently support invisible elements as identity
    # https://github.com/cos-qa/osf-selenium-tests/blob/b7f3f21376b7d6f751993cdcffea9262856263e3/base/locators.py#L138
    meta_tag = driver.find_element_by_xpath(
        '//meta[@property="og:title" and contains(@content, "Support COS")]'
    )

    assert 'support-cos' in driver.current_url
    assert meta_tag.get_attribute('property') == 'og:title'
    assert meta_tag.get_attribute('content') == 'Support COS'

@markers.smoke_test
@markers.core_functionality
class TestCollectionsNavbarLoggedOut():
    @pytest.fixture
    def provider(self, driver):
        return osf_api.get_provider(type='collections', provider_id='selenium')

    @pytest.fixture()
    def collectionsdiscover_page(self, driver, provider):
        discover_page = CollectionDiscoverPage(driver, provider=provider)
        discover_page.goto()
        discover_page.loading_indicator.here_then_gone()
        return discover_page

    def test_search_link(self, driver, collectionsdiscover_page):
        collectionsdiscover_page.search_link.click()
        assert 'discover' in driver.current_url

    def test_donate_link(self, session, driver, collectionsdiscover_page):
        collectionsdiscover_page.donate_link.click()
        donate_page = COSDonatePage(driver, verify=False)
        assert_donate_page(driver, donate_page)

@markers.smoke_test
@markers.core_functionality
@pytest.mark.usefixtures('log_in_if_not_already')
class TestCollectionsNavbarLoggedIn():
    @pytest.fixture
    def provider(self, driver):
        return osf_api.get_provider(type='collections', provider_id='selenium')

    @pytest.fixture()
    def page(self, driver, provider):
        discover_page = CollectionDiscoverPage(driver, provider=provider)
        discover_page.goto()
        discover_page.loading_indicator.here_then_gone()
        return discover_page

    def test_my_projects_link(self, page, driver):
        page.collections_my_projects_link.click()
        assert MyProjectsPage(driver, verify=True)

    def test_add_to_collections_link(self, page, driver):
        page.add_to_collections_link.click()
        assert CollectionSubmitPage(driver, verify=True)

    def test_search_link(self, driver, page):
        page.search_link.click()
        assert 'discover' in driver.current_url

    def test_donate_link(self, session, driver, page):
        page.donate_link.click()
        donate_page = COSDonatePage(driver, verify=False)
        assert_donate_page(driver, donate_page)


@markers.smoke_test
@markers.core_functionality
@pytest.mark.usefixtures('log_in_if_not_already')
class TestProjectsNavbarLoggedIn():
    @pytest.fixture()
    def project_page(self,driver, default_project_page):
         default_project_page.goto()
         return default_project_page

    @pytest.fixture()
    def page(self, driver, project_with_file):
        page = ProjectPage(driver, guid=project_with_file.id)
        page.goto()
        return page

    def test_my_projects_link(self, page, driver, fake):
        page.navbar.projectdetails_my_project_link.click()
        assert MyProjectsPage(driver, verify=True)

    def test_search_link(self, session, driver, page, fake):
        page.navbar.search_link.click()
        SearchPage(driver, verify=True)

    def test_support_link(self, session, driver, page, fake):
        page.navbar.support_link.click()
        SupportPage(driver, verify=True)

    def test_donate_link(self, session, driver, page, fake):
        page.navbar.donate_link.click()
        donate_page = COSDonatePage(driver, verify=False)
        assert_donate_page(driver, donate_page)


