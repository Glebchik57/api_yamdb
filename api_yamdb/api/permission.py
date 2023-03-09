from rest_framework.permissions import IsAuthenticatedOrReadOnly


class UserIsAdmin(IsAuthenticatedOrReadOnly):
    pass
