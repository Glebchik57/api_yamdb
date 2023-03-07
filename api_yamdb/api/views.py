from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, filters, permissions
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import User
from rest_framework import viewsets
from .serializers import UserSerializer, NewUserRegistrationSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    lookup_field = 'username'
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'role']
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        url_name='me',
    )
    def me(self, request, *args, **kwargs):
        if request.method == 'PATCH':
            serializer = NewUserRegistrationSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = NewUserRegistrationSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
