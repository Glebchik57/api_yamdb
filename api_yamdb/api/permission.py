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
