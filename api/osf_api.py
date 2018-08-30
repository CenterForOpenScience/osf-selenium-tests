import settings

from pythosf import client

def get_default_session():
    return client.Session(api_base_url=settings.API_DOMAIN, auth=(settings.USER_ONE, settings.USER_ONE_PASSWORD))

def create_project(session, title='osf selenium test', tags=['qatest']):
    """Create a project for your current user through the OSF api.

    By default, projects will be given the `qatest` tag just in case deleting fails.
    If testing search, you will want to give the project no tags (or different tags).
    """
    node = client.Node(session=session)
    node.create(title=title, tags=tags)
    return node

def current_user(session=None):
    if not session:
        session = get_default_session()
    user = client.User(session=session)
    user.get()
    return user

def get_node(session, node_id=settings.PREFERRED_NODE):
    return client.Node(session=session, id=node_id)

def get_user_institutions(session, user=None):
    if not user:
        user = current_user(session)
    institution_url = user.relationships.institutions['links']['related']['href']
    data = session.get(institution_url)
    institutions = []
    for institution in data['data']:
        institutions.append(institution['attributes']['name'])
    return institutions

def upload_single_quickfile(session):
    """Upload a file to the current user's quickfiles if one is not already uploaded.
    Return the name of the file or none if one wasn't uploaded.

    Note: Currently using v2.0 of the API. Certain lines will need to be changed on update.
    TODO: Make this more general.
    """
    user = current_user(session)
    quickfiles_url = user.relationships.quickfiles['links']['related']['href']
    if session.get(quickfiles_url)['links']['meta']['total'] < 1:
        upload_url = user.relationships.quickfiles['links']['upload']['href']
        return upload_fake_file(session, upload_url=upload_url)

def get_all_institutions(session):
    url = '/v2/institutions/'
    data = session.get(url)
    institutions = []
    for institution in data['data']:
        institutions.append(institution['attributes']['name'])
    return institutions

def delete_all_user_projects(session, user=None):
    """Delete all of your user's projects that they have permission to delete
    except PREFERRED_NODE (if it's set).
    """
    if not user:
        user = current_user(session)
    nodes_url = user.relationships.nodes['links']['related']['href']
    data = session.get(nodes_url)
    for node in data['data']:
        if node['id'] != settings.PREFERRED_NODE:
            n = client.Node(id=node['id'], session=session)
            n.get()
            n.delete()

def get_node_addons(session, node_id):
    """Return a list of the names of all the addons connected to the given node.
    """
    url = '/v2/nodes/{}/files/'.format(node_id)
    data = session.get(url)
    providers = []
    for provider in data['data']:
        providers.append(provider['attributes']['provider'])
    return providers

def waffled_pages(session):
    waffle_list = []
    url = '/v2/_waffle/'
    data = session.get(url)
    for page in data['data']:
        if page['attributes']['active']:
            waffle_list.append(page['attributes']['name'])
    return waffle_list

def get_existing_file(session, node_id=settings.PREFERRED_NODE):
    """Return the name of the first file in OSFStorage on a given node.
    Uploads a new file if one does not exist.
    """
    node = client.Node(session=session, id=node_id)
    node.get()
    files_url = node.relationships.files['links']['related']['href']
    data = session.get(files_url + 'osfstorage/')
    file = data['data']
    if file:
        return data['data'][0]['attributes']['name']
    else:
        return upload_fake_file(session, node)

def upload_fake_file(session, node=None, name='osf selenium test file for testing because its fake.txt', upload_url=None):
    """Upload an almost empty file to the given node. Return the file's name.

    Note: The default file has a very long name because it makes it easier to click a link to it.
    """
    if not upload_url:
        if not node:
            raise TypeError('Node must not be none when upload URL is not set.')
        upload_url = '{}/v1/resources/{}/providers/osfstorage/'.format(settings.FILE_DOMAIN, node.id)

    session.put(url=upload_url, query_parameters={'kind': 'file', 'name': name}, raw_body={})
    return name

def get_providers_list(session=None, type='preprints'):
    """Return the providers list data. The default is the preprint providers list.
    """
    if not session:
        session = get_default_session()
    url = '/v2/providers/' + type
    return session.get(url)['data']
