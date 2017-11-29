from pythosf import client

def create_project(session, title='osf selenium test'):
    node = client.Node(session=session)
    node.create(title=title)
    return node
