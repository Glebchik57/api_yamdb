from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status, filters, permissions
from rest_framework.pagination import LimitOffsetPagination
from django.core.mail import send_mail
from random import randint
from reviews.models import User
from rest_framework import viewsets
from .permission import UserIsAdmin
from .serializers import (UserSerializer,
                          UserRegistrationSerializer,
                          NewUserRegistrationSerializer,
                          TokenSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserIsAdmin]
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
    def me(self, request):
        if request.method == 'PATCH':
            serializer = NewUserRegistrationSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = NewUserRegistrationSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def sign_up(request):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.data
    user = User.objects.filter(username=validated_data['username'])
    confirmation_code = ''.join([str(randint(0, 9)) for i in range(7)])
    if user.exists():
        user = User.objects.filter(
            username=serializer.data['username'],
            email=serializer.data['email'])
        user.confirmation_code = confirmation_code
        for object in user:
            object.save()

        send_mail(
            'Confirmation code',
            confirmation_code,
            'test@example.com',
            recipient_list=[user]
        )
        if not user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(validated_data)
    else:
        serializer = NewUserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.data
        user = serializer.create(validated_data)
        user.confirmation_code = confirmation_code
        user.save()
        send_mail(
            'Confirmation code',
            confirmation_code,
            'test@example.com',
            recipient_list=[user.email]
        )
        return Response({'username': user.username, 'email': user.email})


@api_view(['POST'])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(
        raise_exception=True
    )
    user = get_object_or_404(User, username=serializer.data['username'])
    if serializer.data['confirmation_code'] == user.confirmation_code:
        token = RefreshToken.for_user(user)
        return Response({'token': str(token.access_token)},
                        status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
