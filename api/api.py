import json
import requests

import settings


def create_project(token, title, tags, description, is_public=False, template_from=None):
    """
    Create a project through API V2

    :param token: personal access token of user
    :param title: project title
    :param tags: list of tags of the project
    :param description: project description
    :param is_public: whether the project is public
    :return: the response in JSON of the API call
    """

    payload = {
        'data': {
            'type': 'nodes',
            'attributes': {
                'title': title,
                'category': 'project',
                'description': description,
                'tags': tags,
                'public': is_public,
            }
        }
    }

    if template_from:
        payload['data']['attributes']['template_from'] = template_from

    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(token)
    }

    response = requests.post('{}/{}/'.format(settings.API_DOMAIN, 'nodes'), json.dumps(payload), headers=headers)
    return response.json()

def read_project(token, id):
    """
    Get the project information

    :param token: personal access token
    :param id: project id
    :return: the response in JSON of the API call
    """
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(token)
    }
    url = '{}/{}/'.format(settings.API_DOMAIN, 'nodes')

    response = requests.get(url, headers=headers)
    return response.json()

def update_project(token, id, new_title, new_tags, new_description, is_public):
    """
    Update a project

    :param token: personal access token
    :param id: project id
    :param new_title: new title
    :param new_tags: list of new tags
    :param new_description: new description
    :param is_public: whether the project is public
    :return: the response in JSON of the API call
    """
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(token)
    }
    payload = {
        'data': {
            'type': 'nodes',
            'id': id,
            'attributes': {
                'title': new_title,
                'category': 'project',
                'description': new_description,
                'tags': new_tags,
                'public': is_public,
            }
        }
    }
    url = '{}/{}/{}/'.format(settings.API_DOMAIN, 'nodes', id)

    response = requests.patch(url, json.dumps(payload), headers=headers)
    return response.json()

def delete_project(token, id):
    """
    Delete a project
    :param token: personal access token
    :param id: project id
    :return: the response in JSON of the API call
    """
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(token)
    }
    url = '{}/{}/{}/'.format(settings.API_DOMAIN, 'nodes', id)

    response = requests.delete(url, headers=headers)
    return response.json()