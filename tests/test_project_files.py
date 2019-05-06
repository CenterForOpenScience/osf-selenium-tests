import pytest

#import markers
#import settings
from api import osf_api
from pages.project import FilesPage
#from pages.login import LoginPage, login, logout

@pytest.mark.usefixtures('must_be_logged_in')
class TestFilesPage:

    @pytest.mark.parametrize('provider', ['box'])
    def test_addon(self, driver, default_project, session, provider):
        node_id = default_project.id

        # connect addon to node, upload a single test file
        node = osf_api.get_node(session, node_id=node_id)
        addon = osf_api.get_user_addon(session, provider)
        addon_account_id = list(addon['data']['links']['accounts'])[0]
        osf_api.connect_provider_root_to_node(session, provider, addon_account_id,
                                              node_id=node_id)
        new_file, metadata = osf_api.upload_fake_file(session=session, node=node, name='foo.txt',
                                                      provider=provider)

        files_page = FilesPage(driver, guid=node_id)
        files_page.goto()
        files_page.first_file.present()  # checks files have loaded
        found_it = False
        for row in files_page.fangorn_rows:
            if row.text == new_file:
                found_it = True
                row.find_element_by_xpath('../..').click()  # get grandparent
                break
        assert found_it


# PSEUDO CODE
# select file row in files widget
# click the rename button
# cmd + left to get to beginning of line
# add one more character to name
# hit enter/return to save
# assert verify new name is there

        osf_api.delete_file(session, metadata['data']['links']['delete'])

'''
Next steps:
- Renames
- Deletes
- Checkouts
- Downloads? if there's a way
- Writeable addons that WORK 'box', 'dropbox', 's3' , 'owncloud', 'figshare'
-'googledrive' MUST specify both folder_id and folder_path
-'github' Requested addon not currently configurable via API
-'dataverse' Requested addon not currently configurable via API

'''
