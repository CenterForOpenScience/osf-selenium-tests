import json
import logging
import os
from datetime import datetime

import requests
from pythosf import client

import settings


logger = logging.getLogger(__name__)


def get_default_session():
    return client.Session(
        api_base_url=settings.API_DOMAIN,
        auth=(settings.USER_ONE, settings.USER_ONE_PASSWORD),
    )


def get_user_two_session():
    return client.Session(
        api_base_url=settings.API_DOMAIN,
        auth=(settings.USER_TWO, settings.USER_TWO_PASSWORD),
    )


def create_project(session, title='osf selenium test', tags=None, **kwargs):
    """Create a project for your current user through the OSF api.

    By default, projects will be given the `qatest` tag just in case deleting fails.
    If testing search, you will want to give the project no tags (or different tags).
    """
    if tags is None:
        tags = ['qatest', os.environ['PYTEST_CURRENT_TEST']]
    node = client.Node(session=session)
    node.create(title=title, tags=tags, **kwargs)
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


def get_user_addon(session, provider, user=None):
    """Get list of accounts on the given provider that have already been connected by the user."""
    if not user:
        user = current_user(session)
    addon_url = '/v2/users/{}/addons/{}/'.format(user.id, provider)
    return session.get(addon_url)


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
    for _ in range(3):
        try:
            data = session.get(nodes_url)
        except requests.exceptions.HTTPError as exc:
            if exc.response.status_code == 502:
                logger.warning('502 Exception caught. Re-trying test')
                continue
            raise exc
        else:
            break
    else:
        logger.info('Max tries attempted')
        raise Exception('API not responding. Giving up.')

    nodes_failed = []
    for node in data['data']:
        if node['id'] != settings.PREFERRED_NODE:
            n = client.Node(id=node['id'], session=session)
            try:
                n.get()
                n.delete()
            except Exception as exc:
                nodes_failed.append((node['id'], exc))
                continue

    if nodes_failed:
        error_message_list = []
        for error_tuple in nodes_failed:
            # Position [0] of error_tuple contains node_id
            # Position [1] of error_tuple contains the exception
            error_message = "node '{}' errored with exception: '{}'".format(
                error_tuple[0], error_tuple[1]
            )
            error_message_list.append(error_message)
        logger.error('\n'.join(error_message_list))


def delete_project(session, guid, user=None):
    """Delete a single project. Simply pass in the guid"""
    if not user:
        user = current_user(session)
    nodes_url = user.relationships.nodes['links']['related']['href']
    data = session.get(nodes_url)
    for node in data['data']:
        if node['id'] == guid:
            n = client.Node(id=node['id'], session=session)
            n.get()
            n.delete()


def create_custom_collection(session):
    """Create a new custom collection. You can modify the title of the collection here as well."""
    collections_url = '{}/v2/collections/'.format(session.api_base_url)

    payload = {
        'title': 'Selenium API Custom Collection',
    }

    session.post(collections_url, item_type='collections', attributes=payload)


def delete_custom_collections(session):
    """Delete all custom collections for the current user."""
    collections_url = '{}/v2/collections/'.format(session.api_base_url)
    data = session.get(collections_url)

    for collection in data['data']:
        if not collection['attributes']['bookmarks']:
            collection_self_url = collections_url + collection['id']
            session.delete(url=collection_self_url, item_type=None)


# TODO rename this to get_node_providers, and create new function that actually IS get_node_addons -
#  note, this is confusing, talk to BrianG before we change this
def get_node_addons(session, node_id):
    """Return a list of the names of all the addons connected to the given node."""
    url = '/v2/nodes/{}/files/'.format(node_id)
    data = session.get(url, query_parameters={'page[size]': 20})
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


def upload_fake_file(
    session,
    node=None,
    name='osf selenium test file for testing because its fake.txt',
    upload_url=None,
    provider='osfstorage',
):
    """Upload an almost empty file to the given node. Return the file's name.

    Note: The default file has a very long name because it makes it easier to click a link to it.
    """
    if not upload_url:
        if not node:
            raise TypeError('Node must not be none when upload URL is not set.')
        upload_url = '{}/v1/resources/{}/providers/{}/'.format(
            settings.FILE_DOMAIN, node.id, provider
        )

    metadata = session.put(
        url=upload_url, query_parameters={'kind': 'file', 'name': name}, raw_body={}
    )

    return name, metadata


def delete_addon_files(session, provider, current_browser, guid):
    """Delete all files for the given addon."""
    files_url = '{}/v2/nodes/{}/files/{}/'.format(session.api_base_url, guid, provider)

    data = session.get(url=files_url, query_parameters={'page[size]': 20})

    for file in data['data']:
        if file['attributes']['kind'] == 'file':
            delete_url = file['links']['delete']
            file_name = file['attributes']['name']
            if current_browser in file_name:
                delete_file(session, delete_url)


def delete_file(session, delete_url):
    """Delete a file.  A truly stupid method, caller must provide the delete url from the file
    metadata."""

    # include `item_type=None` b/c pythosf doesn't set a default value for this.
    return session.delete(url=delete_url, item_type=None)


def get_providers_list(session=None, type='preprints'):
    """Return the providers list data. The default is the preprint providers list."""
    if not session:
        session = get_default_session()
    url = '/v2/providers/' + type
    return session.get(url)['data']


def get_provider(session=None, type='registrations', provider_id='osf'):
    """Return the data for an individual provider. The default type is registrations but
    it can also be used for a preprints or collections provider.  The default provider_id
    is 'osf'
    """
    if not session:
        session = get_default_session()
    url = '/v2/providers/' + type + '/' + provider_id
    return session.get(url)['data']


def get_provider_submission_status(provider):
    """Return the boolean attribute `allow_submissions` from the dictionary object (provider)"""
    return provider['attributes']['allow_submissions']


def get_providers_total(provider_name, session):
    """Return the total number of preprints for a given service provider.
    Note: Reformat provider names to all lowercase and remove white spaces.
    """
    provider_url = '/v2/providers/preprints/{}/preprints/'.format(
        provider_name.lower().replace(' ', '')
    )
    return session.get(provider_url)['links']['meta']['total']


def connect_provider_root_to_node(
    session,
    provider,
    external_account_id,
    node_id=settings.PREFERRED_NODE,
):
    """Initialize the node<=>addon connection, add the given external_account_id, and configure it
    to connect to the root folder of the provider."""

    if not session:
        session = get_default_session()

    url = '/v2/nodes/{}/addons/{}/'.format(node_id, provider)

    # Empty POST request "turns it on" (h/t @brianjgeiger). Addon must be configured with a PATCH
    # afterwards.
    # TODO: if box is already connected, will return 400.  Handle that?
    session.post(url=url, item_type='node_addons')

    # This is a workaround for a bug in pythosf v0.0.9 that breaks patch requests.
    # If raw_body is not passed, the session code tries to automatically build the body, which
    # breaks on `item_id`.  If you build the body yourself and pass it in, this bypasses the
    # bug.  When the fix is released, switch to the commented-out block below this.
    raw_payload = {
        'data': {
            'type': 'node_addons',
            'id': provider,
            'attributes': {
                'external_account_id': external_account_id,
                'enabled': True,
            },
        },
    }
    addon = session.patch(
        url=url,
        item_type='node_addons',
        item_id=provider,
        raw_body=json.dumps(raw_payload),
    )
    # payload = {
    #     'external_account_id': external_account_id,
    #     'enabled': True,
    # }
    # addon = session.patch(url=url, item_type='node_addons', item_id=provider,
    #                      attributes=payload)

    # Assume the root folder is the first (and only) folder returned.  Get its id and update
    # the addon config
    root_folder = session.get(url + 'folders/')['data'][0]['attributes']['folder_id']
    raw_payload['data']['attributes']['folder_id'] = root_folder
    addon = session.patch(
        url=url,
        item_type='node_addons',
        item_id=provider,
        raw_body=json.dumps(raw_payload),
    )
    return addon


def get_preprints_list_for_user(session, user=None):
    """Return the list of Preprints for a given user"""
    if not user:
        user = current_user(session)
    url = '/v2/users/{}/preprints/'.format(user.id)
    return session.get(url)['data']


def get_preprint_supplemental_material_guid(session, preprint_guid):
    """Return the Supplemental Material Project guid for a given Preprint"""
    url = '/v2/preprints/{}/relationships/node/'.format(preprint_guid)
    data = session.get(url)['data']
    if data:
        return data['id']
    else:
        return None


def update_node_public_attribute(session, node_id, status=False):
    """Update the public attribute on a given node. This will make a project Private
    if status=False (default) or make the project Public if status=True.
    """
    url = '/v2/nodes/{}/'.format(node_id)
    raw_payload = {
        'data': {
            'type': 'nodes',
            'id': node_id,
            'attributes': {
                'public': status,
            },
        },
    }
    status = session.patch(
        url=url,
        item_type='nodes',
        item_id=node_id,
        raw_body=json.dumps(raw_payload),
    )


def get_most_recent_preprint_node_id(session=None):
    """Return the most recently published preprint node id"""
    if not session:
        session = get_default_session()
    url = '/v2/preprints/'
    data = session.get(url)['data']
    if data:
        for preprint in data:
            if preprint['attributes']['is_published']:
                return preprint['id']
    return None


def get_preprint_views_count(session=None, node_id=None):
    """Return the views count for the given preprint node id"""
    if not session:
        session = get_default_session()
    url = '/v2/preprints/{}/?metrics[views]=total'.format(node_id)
    metadata = session.get(url)['meta']
    if metadata:
        return metadata['metrics']['views']
    else:
        return None


def get_preprint_downloads_count(session=None, node_id=None):
    """Return the downloads count for the given preprint node id"""
    if not session:
        session = get_default_session()
    url = '/v2/preprints/{}/files/osfstorage/'.format(node_id)
    data = session.get(url)['data']
    if data:
        return data[0]['attributes']['extra']['downloads']
    else:
        return None


def get_registration_schemas_for_provider(session=None, provider_id='osf'):
    """Returns a list of allowed registration schemas for an individual provider.  The
    list will be a paired list of schema names and ids.  The The default provider_id is
    'osf'.
    """
    if not session:
        session = get_default_session()
    url = 'v2/providers/registrations/{}/schemas/'.format(provider_id)
    # NOTE: Using '50' as the page size query parameter here. We don't actually have 50
    # total registration schemas. It's under 30 at this time, but using 50 here gives us
    # plenty of room to add more schemas without having to update this function.
    data = session.get(url, query_parameters={'page[size]': 50})['data']
    if data is None:
        return None
    return [[schema['attributes']['name'], schema['id']] for schema in data]


def create_draft_registration(session, node_id=None, schema_id=None):
    """Create a new draft registration for a given project node."""
    if not session:
        session = get_default_session()
    url = '/v2/nodes/{}/draft_registrations/'.format(node_id)
    raw_payload = {
        'data': {
            'type': 'draft_registrations',
            'relationships': {
                'registration_schema': {
                    'data': {
                        'id': schema_id,
                        'type': 'registration-schemas',
                    }
                }
            },
        },
    }
    session.post(
        url=url, item_type='draft_registrations', raw_body=json.dumps(raw_payload)
    )


def create_preprint(
    session,
    provider_id='osf',
    title='OSF Selenium Preprint',
    license_name='CC0 1.0 Universal',
    subject_name='Engineering',
):
    """Creates a new published preprint. There are three main steps in the process:
    1) Create an initial draft unpublished preprint, 2) Create a file in WaterButler and
    associate it to the preprint node, and 3) Update the preprint with the file id from
    WaterButler and set the status of the preprint to Published.
    There are several parameters available to allow more specification in creating the
    preprint. The available parameters and their default values are as follows:
    provider_id='osf'; title='OSF Selenium Preprint'; license_name='CC0 1.0 Universal';
    and subject_name='Engineering'.
    """
    if not session:
        session = get_default_session()
    # Get the license id and any required fields for the license_name parameter
    license_data = get_license_data_for_provider(
        session,
        provider_type='preprints',
        provider_id=provider_id,
        license_name=license_name,
    )
    license_id = license_data[0]
    # If the particular license requires copyright holders then provide some test data
    if 'copyrightHolders' in license_data[1]:
        copyright_holders = ['OSF Selenium Tester', 'QA Guy']
    else:
        copyright_holders = []
    # NOTE: In the preprint payload record below we are adding a license_record with
    # year set to the current year even though in most cases we may be using a license
    # that does not require the year value. There is a weird bug that occurs on the Edit
    # Preprint page if the preprint does not have a value for year. If the year is null
    # then the Edit Preprint page thinks that the preprint has unsaved changes even if
    # you have made no changes on the form page. There is a ticket for this issue:
    # ENG-3782.
    current_year = datetime.now().year
    # Get subject id for the subject_name parameter. NOTE: Currently we are creating
    # the preprint with only a single subject, which is the minimum required to publish.
    subject_id = get_subject_id_for_provider(
        session,
        provider_type='preprints',
        provider_id=provider_id,
        subject_name=subject_name,
    )
    # Step 1: Create draft unpublished preprint without primary file
    url = '/v2/preprints/'
    raw_payload = {
        'data': {
            'type': 'preprints',
            'attributes': {
                'title': title,
                'description': 'Preprint created via the OSF api',
                'subjects': [[subject_id]],
                'license_record': {
                    'copyright_holders': copyright_holders,
                    'year': current_year,
                },
                'tags': ['qatest', 'selenium'],
                'has_coi': False,
                'has_data_links': 'available',
                'data_links': ['https://osf.io/'],
                'has_prereg_links': 'no',
                'why_no_prereg': 'QA Selenium Testing',
            },
            'relationships': {
                'license': {'data': {'type': 'licenses', 'id': license_id}},
                'provider': {'data': {'type': 'providers', 'id': provider_id}},
            },
        }
    }
    return_data = session.post(
        url=url, item_type='preprints', raw_body=json.dumps(raw_payload)
    )
    preprint_node_id = return_data['data']['id']
    # Step 2: Create a test file in WaterButler and associate it with the preprint
    preprint_node = get_node(session, node_id=preprint_node_id)
    file_name, metadata = upload_fake_file(
        session, node=preprint_node, name='OSF Test File.txt', provider='osfstorage'
    )
    # The id value from WB has the provider name and '/' at the beginning of it
    # (ex: 'osfstorage/627a5b3ab4f587000aa2725c').  So we need to parse out the
    # actual file id to use in the Preprint patch.
    file_id = metadata['data']['id'].split('/')[1]
    # Get the moderation type for the Preprint Provider. If the preprint provider
    # uses a moderation workflow (either pre-moderation or post-moderation) then
    # set the should publish flag to False. A pre-moderation preprint cannot be
    # published until after it has been accepted by the moderator, and a post-
    # moderation preprint will automatically get published upon creation of the
    # submit review_action below.
    mod_type = get_moderation_type_for_provider(
        session,
        provider_type='preprints',
        provider_id=provider_id,
    )
    should_publish = mod_type is None
    # Step 3: Attach the file to the Preprint and set the Published status
    patch_url = '/v2/preprints/{}/'.format(preprint_node_id)
    patch_payload = {
        'data': {
            'id': preprint_node_id,
            'type': 'preprints',
            'attributes': {'is_published': should_publish},
            'relationships': {
                'primary_file': {'data': {'type': 'files', 'id': file_id}}
            },
        }
    }
    return_data = session.patch(
        url=patch_url,
        item_type='preprints',
        item_id=preprint_node_id,
        raw_body=json.dumps(patch_payload),
    )
    # If the Preprint Provider uses a moderation workflow (pre-moderation or post-
    # moderation), then create a submit review_action and post it to the preprint
    # record.
    if mod_type is not None:
        review_url = '/v2/preprints/{}/review_actions/'.format(preprint_node_id)
        review_payload = {
            'data': {
                'type': 'review_actions',
                'attributes': {'trigger': 'submit'},
                'relationships': {
                    'target': {'data': {'id': preprint_node_id, 'type': 'preprints'}}
                },
            }
        }
        session.post(
            url=review_url,
            item_type='review-actions',
            raw_body=json.dumps(review_payload),
        )
    # Return the Preprint Node Id
    return return_data['data']['id']


def get_license_data_for_provider(
    session=None,
    provider_type='preprints',
    provider_id='osf',
    license_name='CC0 1.0 Universal',
):
    """Returns the license id and any required fields for a given provider type, provider
    id, and license name. Required fields may be 'year' and 'copyrightHolders' for some
    licenses. The default provider_type is 'preprints' but this will also work for
    'registrations'. The default provider_id is 'osf' and the default license_name is
    'CC0 1.0 Universal'.
    """
    if not session:
        session = get_default_session()
    url = 'v2/providers/{}/{}/licenses/'.format(provider_type, provider_id)
    # NOTE: Using '30' as the page size query parameter here. We don't actually have 30
    # total licenses. It's under 20 at this time, but using 30 here gives us plenty of
    # room to add more licenses without having to update this function.
    data = session.get(url, query_parameters={'page[size]': 30})['data']
    for license in data:
        if license['attributes']['name'] == license_name:
            license_id = license['id']
            required_fields = license['attributes']['required_fields']
            break
    return [license_id, required_fields]


def get_subject_id_for_provider(
    session=None,
    provider_type='preprints',
    provider_id='osf',
    subject_name='Engineering',
):
    """Returns the subject id for a given provider type, provider id, and subject name.
    The default provider_type is 'preprints' but this will also work for 'registrations'.
    The default provider_id is 'osf' and the default subject_name is 'Engineering'.
    """
    if not session:
        session = get_default_session()
    url = 'v2/providers/{}/{}/subjects/'.format(provider_type, provider_id)
    # NOTE: Using '1000' as the page size query parameter here. Not sure how many
    # subjects actually exist for a given provider.
    data = session.get(url, query_parameters={'page[size]': 1000})['data']
    for subject in data:
        if subject['attributes']['text'] == subject_name:
            subject_id = subject['id']
            break
    return subject_id


def get_preprint_requests_records(session=None, node_id=None):
    """Return the requests records for a given preprint node_id"""
    if not session:
        session = get_default_session()
    url = 'v2/preprints/{}/requests/'.format(node_id)
    data = session.get(url)['data']
    if data:
        return data
    else:
        return None


def get_moderation_type_for_provider(
    session=None,
    provider_type='preprints',
    provider_id='osf',
):
    """Returns the moderation type for a given provider type and provider id.  The
    default provider_type is 'preprints' but this will also work for 'registrations'.
    The default provider_id is 'osf'.
    """
    if not session:
        session = get_default_session()
    url = 'v2/providers/{}/{}/'.format(provider_type, provider_id)
    data = session.get(url)['data']
    if data:
        return data['attributes']['reviews_workflow']
    return None


def get_preprint_publish_and_review_states(session=None, preprint_node=None):
    """Return the publish and review states for the given preprint node id"""
    if not session:
        session = get_default_session()
    url = '/v2/preprints/{}/'.format(preprint_node)
    data = session.get(url)['data']
    if data:
        publish_state = data['attributes']['is_published']
        review_state = data['attributes']['reviews_state']
        return [publish_state, review_state]
    return None


def accept_moderated_preprint(session=None, preprint_node=None):
    """Accept a moderated preprint by creating an 'accept' review_action record for a
    given preprint node id.
    """
    if not session:
        session = get_default_session()
    review_url = '/v2/preprints/{}/review_actions/'.format(preprint_node)
    review_payload = {
        'data': {
            'type': 'review_actions',
            'attributes': {
                'trigger': 'accept',
                'comment': 'Preprint Accepted via OSF api',
            },
            'relationships': {
                'target': {'data': {'id': preprint_node, 'type': 'preprints'}}
            },
        }
    }
    session.post(
        url=review_url,
        item_type='review-actions',
        raw_body=json.dumps(review_payload),
    )


def create_preprint_withdrawal_request(session=None, preprint_node=None):
    """Create a withdrawal request for a given preprint node id."""
    if not session:
        session = get_default_session()
    url = '/v2/preprints/{}/requests/'.format(preprint_node)
    request_payload = {
        'data': {
            'type': 'preprint-requests',
            'attributes': {
                'request_type': 'withdrawal',
                'comment': 'Withdrawal Request via OSF api',
            },
            'relationships': {
                'target': {'data': {'id': preprint_node, 'type': 'preprints'}}
            },
        }
    }
    session.post(
        url=url,
        item_type='preprint-requests',
        raw_body=json.dumps(request_payload),
    )


def create_user_developer_app(
    session,
    name='OSF Test Dev App',
    description=None,
    home_url=settings.OSF_HOME,
    callback_url=settings.OSF_HOME,
):
    """Create a Developer Application for the user that is currently logged in to OSF
    (via session object).
    """
    if not session:
        session = get_default_session()
    url = '/v2/applications/'
    raw_payload = {
        'data': {
            'type': 'applications',
            'attributes': {
                'name': name,
                'description': description,
                'home_url': home_url,
                'callback_url': callback_url,
            },
        }
    }
    return_data = session.post(
        url=url, item_type='applications', raw_body=json.dumps(raw_payload)
    )
    # Return the application id
    if return_data:
        return return_data['data']['id']
    return None


def delete_user_developer_app(session, app_id=None):
    """Delete a User's Developer Application as identified by its application id."""
    if not session:
        session = get_default_session()
    url = '/v2/applications/{}/'.format(app_id)
    session.delete(url=url, item_type='applications')


def get_user_developer_app_data(session, app_id=None):
    """Return User Developer Application data for a given application id."""
    if not session:
        session = get_default_session()
    url = '/v2/applications/{}/'.format(app_id)
    data = session.get(url)['data']
    if data:
        return data
    return None


def create_personal_access_token(
    session, name='OSF Test PAT', scopes='osf.nodes.full_read'
):
    """Create a Personal Access Token for the user that is currently logged in to OSF
    (via session object). Default scope is 'osf.nodes.full_read'. The scopes parameter
    is a string (not a list) with multiple scopes separated by a space.
    EX: 'osf.users.profile_write osf.full_write osf.nodes.full_write'
    """
    if not session:
        session = get_default_session()
    url = '/v2/tokens/'
    raw_payload = {
        'data': {
            'type': 'tokens',
            'attributes': {
                'name': name,
                'scopes': scopes,
            },
        }
    }
    return_data = session.post(
        url=url, item_type='tokens', raw_body=json.dumps(raw_payload)
    )
    # Return the token id
    if return_data:
        return return_data['data']['id']
    return None


def delete_personal_access_token(session, token_id=None):
    """Delete a User's Personal Access Token as identified by its token id."""
    if not session:
        session = get_default_session()
    url = '/v2/tokens/{}/'.format(token_id)
    session.delete(url=url, item_type='tokens')


def get_user_pat_data(session, token_id=None):
    """Return User Personal Access Token data for a given token id."""
    if not session:
        session = get_default_session()
    url = '/v2/tokens/{}/'.format(token_id)
    data = session.get(url)['data']
    if data:
        return data
    return None
