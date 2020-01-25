from __future__ import unicode_literals


class CurrentRequestItemDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['requested_item']

    def __repr__(self):
        return '%s()' % self.__class__.__name__
