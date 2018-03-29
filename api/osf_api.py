import settings
from pythosf import client

def create_project(session, title='osf selenium test'):
    node = client.Node(session=session)
    node.create(title=title)
    return node

def current_user(session):
    user = User(session=session)
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


class User(client.APIDetail):
    def __init__(self, session, id=None, self_link=None, data=None):
        super().__init__(session=session, data=data)
        if not data:
            self.id = id
            self.type = 'users'
            self.links = None
            self.meta = None
            self.self_link = self_link
        self.providers = []

    def get(self, query_parameters=None, token=None):
        url = '/v2/users/me/'
        if self.self_link:
            url = self.self_link
        elif self.links:
            url = self.links.self
        elif self.id:
            url = '/v2/users/{}/'.format(self.id)

        response = self.session.get(url=url, query_parameters=query_parameters, token=token)
        if response:
            self._update(response=response)
        else:
            raise ValueError('No url or id to get. Set the id or self_link then try to get.')
