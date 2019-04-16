import pytest

#import markers
#import settings
from api import osf_api
from pages.project import FilesPage
#from pages.login import LoginPage, login, logout


@pytest.mark.usefixtures('must_be_logged_in')
class TestFilesPage:

    def test_addon(self, driver, default_project, session):
        node_id = default_project.id

        # connect addon to node, upload a single test file
        node = osf_api.get_node(session, node_id=node_id)
        box_addon = osf_api.get_user_addon(session, 'box')
        box_account_id = list(box_addon['data']['links']['accounts'])[0]
        osf_api.connect_provider_root_to_node(session, 'box', box_account_id,
                                              node_id=node_id)
        new_file = osf_api.upload_fake_file(session=session, node=node, name='foo.txt',
                                            provider='box')

        files_page = FilesPage(driver, guid=node_id)
        files_page.goto()
        files_page.first_file.present()  # checks files have loaded
        found_it = False
        for row in files_page.fangorn_rows:
            if row.text == new_file:
                found_it = True
        assert found_it

        #TODO write steps to delete file at end of test
        #TODO figure out programmatic way to connect/configure Box to test project

        #TODO if we're creating the project at the beginning of test, then, should delete project at end of test

        """
        FUTURE TEST STEPS

        Create a project (√)
            # project_one = osf_api.create_project(FilesPage.session, title='Files Test Project')
            # assert project_one.title=='Files Test Project'
        Connect Box to project, connect folder "selenium" to project
            ^ Do we need a special patch for this??
            ^^ could be: node/node_id/addons/box/ POST
        Get Box folder "selenium" from OSF API
            # providers=osf_api.get_node_addons(FilesPage.session, node_id)
        Via osf.api create/upload text file (one step) to Box folder "selenium"
        Assert name of file is present in files widget (√)
        """
        #TODO use Lauren's thingy that makes a random name for the project
