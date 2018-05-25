import settings
from pythosf import client

def create_project(session, title='osf selenium test'):
    node = client.Node(session=session)
    node.create(title=title)
    return node

def current_user(session):
    user = client.User(session=session)
    user.get()
    return user

def get_user_institutions(session, user=None):
    if not user:
        user = current_user(session)
    institution_url = user.relationships.institutions['links']['related']['href']
    data = session.get(institution_url)
    institutions = []
    for institution in data['data']:
        institutions.append(institution['attributes']['name'])
    return institutions

def get_all_institutions(session):
    url = '/v2/institutions/'
    data = session.get(url)
    institutions = []
    for institution in data['data']:
        institutions.append(institution['attributes']['name'])
    return institutions

def delete_all_user_projects(session, user=None):
    if not user:
        user = current_user(session)
    nodes_url = user.relationships.nodes['links']['related']['href']
    data = session.get(nodes_url)
    for node in data['data']:
        n = client.Node(id=node['id'], session=session)
        n.get()
        n.delete()

def waffled_pages(session):
    waffle_list = []
    url = '/v2/_waffle/'
    data = session.get(url)
    for page in data['data']:
        if page['attributes']['active']:
            waffle_list.append(page['attributes']['name'])
    return waffle_list

def upload_fake_file(session, node, name='osf selenium test file for testing because its fake.txt'):
    # Note: I gave this file a long name because it makes it easier to click if it takes up more space
    session.put(url='{}/v1/resources/{}/providers/osfstorage/'.format(settings.FILE_DOMAIN, node.id), query_parameters={'kind': 'file', 'name': name}, raw_body={})
    return name
