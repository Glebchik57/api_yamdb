from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class UserIsAdmin(IsAuthenticatedOrReadOnly):

    def has_permission(self, request, view):
        return ((request.user.is_authenticated
                and request.user.role == 'admin')
                or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return ((request.user.is_authenticated
                and request.user.role == 'admin')
                or request.user.is_superuser)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Разрешение редактировать объект только владельцу"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
