import pytest
import settings
from api import osf_api
from pythosf import client
from pages.login import logout, login
from utils import launch_driver


@pytest.fixture(scope='session')
def session():
    return client.Session(api_base_url=settings.API_DOMAIN, auth=(settings.USER_ONE, settings.USER_ONE_PASSWORD))

@pytest.fixture(scope='session', autouse=True)
def check_credentials(session):
    # This only checks if your API key is correct, not if you can log in
    try:
        osf_api.current_user(session)
    except Exception:
        pytest.exit('Your user credentials are incorrect.')

@pytest.fixture(scope='session')
def driver():
    driver = launch_driver()
    yield driver
    driver.quit()

@pytest.fixture(scope='session', autouse=True)
def waffled_pages(session):
    settings.EMBER_PAGES = osf_api.waffled_pages(session)

@pytest.fixture(scope='class', autouse=True)
def default_logout(driver):
    logout(driver)

# TODO: Possibly return to safe_login in the future
@pytest.fixture(scope='class')
def must_be_logged_in(driver):
    login(driver)

@pytest.fixture(scope='class')
def delete_user_projects_at_setup(session):
    osf_api.delete_all_user_projects(session=session)

@pytest.fixture
def default_project(session):
    project = osf_api.create_project(session, title='OSF Test Project')
    yield project
    project.delete()
