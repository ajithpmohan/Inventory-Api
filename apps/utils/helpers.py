from __future__ import unicode_literals


def default_content_path(instance, filename):
    return '/'.join([instance.__class__.__name__.lower(), filename])
