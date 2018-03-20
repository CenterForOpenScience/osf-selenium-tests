import pytest
import settings
from pythosf import client
from api import osf_api as osf
from utils import launch_driver
from pages.login import logout, safe_login


@pytest.fixture(scope='session', autouse=True)
def check_credentials():
    # This only checks if your API key is correct, not if you can log in
    session = client.Session(api_base_url=settings.API_DOMAIN, token=settings.USER_ONE_TOKEN)
    try:
        osf.current_user(session)
    except Exception:
        pytest.exit('Your user credentials are incorrect.')

@pytest.fixture(scope='session')
def driver():
    driver = launch_driver()
    yield driver
    driver.quit()

@pytest.fixture(scope='session')
def session():
    return client.Session(api_base_url=settings.API_DOMAIN, token=settings.USER_ONE_TOKEN)

@pytest.fixture(scope='class', autouse=True)
def default_logout(driver):
    logout(driver)

@pytest.fixture(scope='class')
def must_be_logged_in(driver):
    safe_login(driver)


@pytest.fixture(scope='class')
def delete_user_projects_at_setup(session):
    osf.delete_all_user_projects(session=session)
