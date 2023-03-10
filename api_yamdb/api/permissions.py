from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Разрешение редактировать объект только владельцу"""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS or (
                request.user.is_authenticated and (
                    obj.author == request.user
                    or request.user.role == 'moderator'
                    or request.user.role == 'admin'
                )
            )
        )


class UserIsAdmin(IsAuthenticatedOrReadOnly):

    def has_permission(self, request, view):
        return ((request.user.is_authenticated
                 and request.user.role == 'admin')
                or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return ((request.user.is_authenticated
                 and request.user.role == 'admin')
                or request.user.is_superuser)


class OtherReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
