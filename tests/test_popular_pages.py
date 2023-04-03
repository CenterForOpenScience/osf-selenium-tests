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
        The list of pages are contained in an external text file to make it easier to
        maintain.  Only one page should be entered on each line in the file and each
        line should begin with the OSF object type (project, preprint, or registration)
        followed by a : and then the guid of the object. EX: 'project:ef53g'. The test
        will process every line in the file and attempt to load every page before any
        error is thrown.  After the entire file has been read, if there were any errors
        the test will fail and display a list of all of the pages that failed to load.
        """
        file = open('test_data/popular_pages.txt')

        failed_list = []
        for line in file.readlines():
            segments = line.split(':')
            page_type = segments[0]
            guid = segments[1]
            if page_type == 'project':
                try:
                    project_page = ProjectPage(driver, guid=guid)
                    project_page.goto()
                    assert ProjectPage(driver, verify=True)
                except PageException:
                    failed_list.append(line)
            elif page_type == 'preprint':
                try:
                    preprint_page = PreprintDetailPage(driver, guid=guid)
                    preprint_page.goto()
                    assert PreprintDetailPage(driver, verify=True)
                except PageException:
                    failed_list.append(line)
            elif page_type == 'registration':
                try:
                    registration_page = RegistrationDetailPage(driver, guid=guid)
                    registration_page.goto()
                    assert RegistrationDetailPage(driver, verify=True)
                except PageException:
                    failed_list.append(line)
            else:
                # Not one of the valid object types so add to the error list
                failed_list.append('Not a valid object type - ' + line)

        # If there were any page load failures then fail the test and print the lines
        # that failed
        assert len(failed_list) == 0, 'The following Pages Failed: ' + str(failed_list)

        file.close()
