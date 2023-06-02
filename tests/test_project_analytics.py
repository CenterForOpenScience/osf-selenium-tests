from datetime import (
    datetime,
    timezone,
)

import pytest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import markers
import settings
from api import osf_api
from pages.project import (
    AnalyticsPage,
    FilesPage,
    ProjectPage,
)


@markers.smoke_test
class TestAnalyticsPage:
    def test_private_project(self, driver, default_project, must_be_logged_in):
        """Test the Analytics page on a Private Project. A message should display at the
        top of the page indicating that the project is Private and that Analytics are not
        available and the graphs should be disabled and blurred.
        """
        analytics_page = AnalyticsPage(driver, guid=default_project.id)
        analytics_page.goto()
        analytics_page.loading_indicator.here_then_gone()
        assert analytics_page.private_project_message.present()
        # Existing bug - ENG-4456 - Graphs on Private Projects should be Disabled
        # assert analytics_page.disabled_chart.present()


def parse_node_analytics_data(raw_data, request, **kwargs):
    """Helper function that takes the raw data from the OSF api metrics Node Analytics
    query and returns a specific piece of data. The Node Analytics query is meant to be
    used by the Project Analytics page to gather metrics data to build the various
    graphs on that page for Public projects.
    """
    if request == 'page_view_count':
        # Popular Page Visits count data contains the top 10 most popular pages
        page = kwargs.get('page')
        popular_pages = raw_data['attributes']['popular_pages']
        # Initialize the page count value to 0 and only override it if there is a
        # value found in the data.
        page_count = 0
        for page_data in popular_pages:
            if page == 'home' or page == 'node':
                node_id = kwargs.get('node_id')
                if page_data['path'] == '/{}'.format(node_id):
                    page_count = page_data['count']
                    break
            elif page == 'files':
                # For Files page count, visits to the various storage provider addons
                # are aggregated in the graph.
                if 'files' in page_data['path']:
                    page_count = page_count + page_data['count']
            elif page == 'wiki':
                # For Wiki page count, visits to any individual wiki pages are
                # aggregated in the graph.
                if 'wiki' in page_data['path']:
                    page_count = page_count + page_data['count']
            elif page in page_data['path']:
                page_count = page_data['count']
                break
        return page_count
    elif request == 'unique_visits_count':
        # Unique Visits Count is a list by Date in format: YYYY-MM-DD (in UTC timezone)
        date = kwargs.get('date')
        unique_visits = raw_data['attributes']['unique_visits']
        # Initialize the visit count value to 0 and only override it if there is a
        # value found in the data.
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
        # found in the data.
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
        # value found in the data.
        referrer_count = 0
        for referrer in referrer_domains:
            if referrer['referer_domain'] == domain:
                referrer_count = referrer['count']
                break
        return referrer_count


@pytest.fixture()
def public_project_node(session, driver):
    """Returns the project node id for a Public project in OSF"""
    return osf_api.get_most_recent_public_node_id(session)


@markers.smoke_test
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

        # Get the unique visits count data from the api
        visit_data = osf_api.get_project_node_analytics_data(
            session, node_id=public_project_node
        )
        now = datetime.now(timezone.utc)
        date_today = now.strftime('%Y-%m-%d')
        visits_count = parse_node_analytics_data(
            visit_data, 'unique_visits_count', date=date_today
        )

        # Next navigate to the Analytics page for the project.
        analytics_page = AnalyticsPage(driver, guid=public_project_node)
        analytics_page.goto_with_reload()
        analytics_page.loading_indicator.here_then_gone()

        analytics_page.scroll_into_view(
            analytics_page.unique_visits_week_current_day_point.element
        )

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

        # Verify that the value displayed in the tool tip matches the value from the api
        # allowing for a difference of up to 1 since slower machines (i.e. BrowserStack)
        # may cause the graph to load slower and thus may include the current visit to
        # the Analytics page.
        assert abs(unique_visits_display - visits_count) <= 1

    def test_tod_visits_graph(self, session, driver, public_project_node):
        """Test the Time of Day of Visits Graph on the Project Analytics page. First
        retrieve the metrics data for a public project using the OSF api and then go to
        the Analytics page for the project.  Verify that the value displayed for the
        current time of day on the Time of Day of Visits Graph matches the expected
        value from the api. NOTE: For this test we will change the date range to Two
        Weeks (aka fortnight).
        """

        # First navigate to the Project Overview page for the project so that there
        # will be at least 1 registered visit for the current time of day on the graph.
        project_page = ProjectPage(driver, guid=public_project_node)
        project_page.goto()
        project_page.loading_indicator.here_then_gone()

        # Get the Time of Day visits count data from the api
        visit_data = osf_api.get_project_node_analytics_data(
            session, node_id=public_project_node, timespan='fortnight'
        )
        now = datetime.now(timezone.utc)
        current_hour = int(now.strftime('%H'))
        tod_count = parse_node_analytics_data(
            visit_data, 'time_of_day_count', hour=current_hour
        )

        # Navigate to the Analytics page for the project using the Two Weeks (fortnight)
        # time span parameter in order to avoid the Analytics page reload that occurs
        # when the date range is changed on the page.
        url = settings.OSF_HOME + '/{}/analytics?timespan=fortnight'.format(
            public_project_node
        )
        driver.get(url)
        analytics_page = AnalyticsPage(driver, verify=True)
        analytics_page.loading_indicator.here_then_gone()

        # Hover the mouse over the bar on the Time of Day of Visits graph that
        # represents the current hour of the day and get the value that is displayed
        # in the tool tip.
        current_hour_bar = analytics_page.get_tod_bar_by_hour(current_hour)
        analytics_page.scroll_into_view(current_hour_bar)
        action_chains = ActionChains(driver)
        action_chains.move_to_element(current_hour_bar).perform()
        WebDriverWait(driver, 3).until(
            EC.visibility_of(analytics_page.tod_visits_tooltip_value)
        )
        tod_visits_display = int(analytics_page.tod_visits_tooltip_value.text)

        # Verify that the value displayed in the tool tip matches the value from the api
        # allowing for a difference of up to 1 since slower machines (i.e. BrowserStack)
        # may cause the graph to load slower and thus may include the current visit to
        # the Analytics page.
        assert abs(tod_visits_display - tod_count) <= 1

    # NOTE: At this time we are not creating a test for the Top Referrers Graph. The
    # primary reason is that through Selenium there is no referrer registered. So there
    # could be the case that with a brand new public project there would be no referrer
    # metrics data and therefore no graph. Maybe we could engineer a referrer by
    # creating a link to the node and adding it to another project or even to an
    # external website like GitHub and then using the link to go to the project. This
    # feels like an unnecessary stretch and not worth the effort at this time.

    def test_popular_pages_graph(self, session, driver, public_project_node):
        """Test the Popular Pages Graph on the Project Analytics page. First navigate
        to the Analytics page for a public project and determine the most visited page
        on the Popular Pages graph. Next get the metrics data for the project and use
        the label for the most popular page bar to get the page visit count from the
        metrics data. Then verify that the page count displayed on the graph matches
        the value in the metrics data. NOTE: For this test we will change the date
        range to 1 month.
        """

        # Navigate to the Analytics page for the project using the month time span
        # parameter in order to avoid the Analytics page reload that occurs when the
        # date range is changed on the page.
        url = settings.OSF_HOME + '/{}/analytics?timespan=month'.format(
            public_project_node
        )
        driver.get(url)
        analytics_page = AnalyticsPage(driver, verify=True)
        analytics_page.loading_indicator.here_then_gone()

        # Scroll down and get the label for the most popular page (top bar) from the
        # Popular Pages graph
        analytics_page.scroll_into_view(analytics_page.most_visited_page_label.element)
        page_label = analytics_page.most_visited_page_label.text
        if page_label[5:11] == ': Home':
            # For individual File nodes or Component nodes the label is '<guid>: Home'
            # NOTE: There is an open PR for this ENG-4455 to change the labels for File
            # and Component nodes to be clearer. At some point these labels will change
            # and this test will need to be updated to reflect that change, whatever it
            # ends up being.
            parse_node = page_label[0:5]
            parse_page = 'node'
        else:
            parse_node = public_project_node
            parse_page = page_label.lower()

        # Get the project's metrics data for the last month from the api
        visit_data = osf_api.get_project_node_analytics_data(
            session, node_id=public_project_node, timespan='month'
        )

        # Parse the metrics data to get the page views count for the most popular page
        visit_count = parse_node_analytics_data(
            visit_data, 'page_view_count', page=parse_page, node_id=parse_node
        )

        # Hover the mouse over the top bar on the Popular Pages graph which represents
        # the most popular page and get the value that is displayed in the tool tip.
        action_chains = ActionChains(driver)
        action_chains.move_to_element(
            analytics_page.most_visited_page_bar.element
        ).perform()
        WebDriverWait(driver, 3).until(
            EC.visibility_of(analytics_page.popular_pages_tooltip_value)
        )
        visit_display = int(analytics_page.popular_pages_tooltip_value.text)

        if page_label == 'Analytics':
            # If the most visited page is the Analytics page then increment the display
            # count by 1 in order to count the current visit
            visit_display = visit_display + 1

        assert abs(visit_display - visit_count) <= 1
