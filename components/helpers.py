def format_addon_name(addon_id):
    """Helper function that returns a formatted addon name for a given addon id"""
    if addon_id == 's3':
        return 'Amazon S3'
    elif addon_id == 'osfstorage':
        return 'OSF Storage'
    elif addon_id == 'owncloud':
        return 'ownCloud'
    else:
        # Capitalize all others (i.e. 'Box', 'Dropbox')
        return addon_id.capitalize()
