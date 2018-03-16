import pytest
import settings
from pythosf import client
from api import osf_api as osf


@pytest.fixture(scope='session', autouse=True)
def check_credentials():
    # This only checks if your API key is correct, not if you can log in
    session = client.Session(api_base_url=settings.API_DOMAIN, token=settings.USER_ONE_TOKEN)
    try:
        osf.current_user(session)
    except Exception:
        pytest.exit('Your user credentials are incorrect.')
