from __future__ import unicode_literals

from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsNotAdminUserReadOnly(BasePermission):
    """
    The request is authenticated as a user and not a staff, then is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS and
            request.user and
            request.user.is_authenticated and
            not request.user.is_staff
        )


class IsNotAdminUser(BasePermission):
    """
    Allows access only to non staff users.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            not request.user.is_staff
        )


class IsAdminUserReadOnly(BasePermission):
    """
    Allows read only access to staff users.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS and
            request.user and
            request.user.is_authenticated and
            request.user.is_staff
        )
