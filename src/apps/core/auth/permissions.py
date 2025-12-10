from rest_framework.permissions import BasePermission

from apps.core.services.model_status import UserType


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    Works with JWTAuthentication.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsAdmin(BasePermission):
    """
    Only admin users can access.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == UserType.ADMIN
        )


class IsSuperAdmin(BasePermission):
    """
    Only superusers.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == UserType.SUPERADMIN
        )
