import pytest

import markers
import settings
from base.exceptions import PageException
from pages.preprints import PreprintDetailPage
from pages.project import ProjectPage
from pages.registries import RegistrationDetailPage


@pytest.mark.skipif(
    not settings.PRODUCTION,
    reason='This test is only for the Two Minute Drill in Production',
)
@markers.two_minute_drill
class TestPopularPages:
    def test_popular_pages_load(self, driver):
        """Test that ensures certain popular pages in OSF Production load correctly.
        The list of pages are contained in the environment variable POPULAR_PAGES.
        Each page in the list should begin with the OSF object type (project, preprint,
        or registration) followed by a : and then the guid of the object. EX: 'project:abcde'.
        The test will process every list item and attempt to load every page before any
        error is thrown.  After the entire list has been processed, if there were any
        errors the test will fail and display a list of all of the pages that failed
        to load.
        """
        popular_pages = settings.POPULAR_PAGES

        failed_list = []
        for page in popular_pages:
            segments = page.split(':')
            page_type = segments[0]
            guid = segments[1]

            # Set page class type
            if page_type == 'project':
                page_class = ProjectPage(driver, guid=guid)
            elif page_type == 'preprint':
                page_class = PreprintDetailPage(driver, guid=guid)
            elif page_type == 'registration':
                page_class = RegistrationDetailPage(driver, guid=guid)
            else:
                # Not one of the valid object types so add to the error list
                failed_list.append('Not a valid object type - ' + page)

            try:
                page_class.goto()
                assert page_class.verify()
            except PageException:
                failed_list.append(page)

        # If there were any page load failures then fail the test and print the lines
        # that failed
        assert len(failed_list) == 0, 'The following Pages Failed: ' + str(failed_list)
