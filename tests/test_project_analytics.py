from datetime import (
    datetime,
    timezone,
)

import pytest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from api import osf_api
from pages.project import (
    AnalyticsPage,
    FilesPage,
)


def parse_node_analytics_data(raw_data, request, **kwargs):
    """Helper function that takes the raw data from the OSF api metrics Node Analytics
    query and returns a specific piece of data. The Node Analytics query is meant to be
    used by the Project Analytics page to gather metrics data to build the various
    graphs on that page for Public projects.
    """
    if request == 'page_view_count':
        # The pages available to public view are: 'overview', 'metadata', 'files',
        # 'wiki', 'analytics', and 'registrations'.
        page = kwargs.get('page', 'overview')
        popular_pages = raw_data['attributes']['popular_pages']
        # Initialize the page count value to 0 and only override it if there is a
        # value found in the data. New temporary projects will not have any data for
        # page views yet.
        page_count = 0
        for page_data in popular_pages:
            if page == 'overview':
                node_id = kwargs.get('node_id')
                if page_data['path'] == '/{}'.format(node_id):
                    page_count = page_data['count']
                    break
            elif page in page_data['path']:
                page_count = page_data['count']
        return page_count
    elif request == 'unique_visits_count':
        # Unique Visits Count is a list by Date in format: YYYY-MM-DD (in UTC timezone)
        date = kwargs.get('date')
        unique_visits = raw_data['attributes']['unique_visits']
        # Initialize the visit count value to 0 and only override it if there is a
        # value found in the data. New temporary projects will not have any data for
        # unique visits yet.
        visit_count = 0
        for visit in unique_visits:
            if visit['date'] == date:
                visit_count = visit['count']
                break
        return visit_count
    elif request == 'time_of_day_count':
        # Time of Day Count is a list of visits per hour (in UTC timezone)
        hour = kwargs.get('hour')
        time_of_day = raw_data['attributes']['time_of_day']
        # Initialize the tod count value to 0 and only override it if there is a value
        # found in the data. New temporary projects will not have any data for time of
        # day visits yet.
        tod_count = 0
        for tod in time_of_day:
            if tod['hour'] == hour:
                tod_count = tod['count']
                break
        return tod_count
    elif request == 'referrer_domain_count':
        domain = kwargs.get('domain')
        referrer_domains = raw_data['attributes']['referer_domain']
        # Initialize the referrer count value to 0 and only override it if there is a
        # value found in the data. New temporary projects will not have any data for
        # the referrer domain count yet.
        referrer_count = 0
        for referrer in referrer_domains:
            if referrer['referer_domain'] == domain:
                referrer_count = tod['count']
                break
        return referrer_count


@pytest.fixture()
def public_project_node(session, driver):
    """Returns the project node id for a Public project in OSF"""
    return osf_api.get_most_recent_public_node_id(session)


@pytest.mark.usefixtures('hide_footer_slide_in')
class TestNodeAnalytics:
    def test_unique_visits_graph(self, session, driver, public_project_node):
        """Test the Unique Visits Graph on the Project Analytics page. First retrieve
        the metrics data for a public project using the OSF api and then go to the
        Analytics page for the project.  Verify that the value displayed for the current
        day on the Unique Visits Graph matches the expected value from the api.
        NOTE: For this test we will not change the default date range of 1 week.
        """

        # First navigate to the Files page for the project so that there will be at
        # least 1 registered visit on the graph
        files_page = FilesPage(
            driver, guid=public_project_node, addon_provider='osfstorage'
        )
        files_page.goto()
        files_page.loading_indicator.here_then_gone()

        # Get the Before unique visits count data from the api
        before_data = osf_api.get_project_node_analytics_data(
            session, node_id=public_project_node
        )
        now = datetime.now(timezone.utc)
        date_today = now.strftime('%Y-%m-%d')
        before_visits_count = parse_node_analytics_data(
            before_data, 'unique_visits_count', date=date_today
        )

        # Next navigate to the Analytics page for the project.
        analytics_page = AnalyticsPage(driver, guid=public_project_node)
        analytics_page.goto()
        analytics_page.loading_indicator.here_then_gone()

        # Hover the mouse over the point on the Unique Visits graph that represents the
        # current day and get the value that is displayed in the tool tip.
        action_chains = ActionChains(driver)
        action_chains.move_to_element(
            analytics_page.unique_visits_week_current_day_point.element
        ).perform()
        WebDriverWait(driver, 3).until(
            EC.visibility_of(analytics_page.unique_visits_tooltip_value)
        )
        unique_visits_display = int(analytics_page.unique_visits_tooltip_value.text)
        assert unique_visits_display == before_visits_count

        # Retrieve the metrics data again and verify that it now registers an additional
        # unique visit since we went to the Analytics page.
        after_data = osf_api.get_project_node_analytics_data(
            session, node_id=public_project_node
        )
        after_visits_count = parse_node_analytics_data(
            after_data, 'unique_visits_count', date=date_today
        )
        assert after_visits_count == before_visits_count + 1
