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

#TODO: Rewrite these things so they can come from pythosf
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

def waffled_pages():
    waffle_list = []
    url = '/v2/_waffle/'
    session = client.Session(api_base_url=settings.API_DOMAIN)
    data = session.get(url)
    for page in data['data']:
        if page['attributes']['active']:
            waffle_list.append(page['attributes']['name'])
    return waffle_list
