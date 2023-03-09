from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework import status, filters, permissions
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from random import randint

from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Titles, Review, User, Categories, Genres, Titles
from .serializers import (
    ReviewSerializer,
    CommentSerializer,
    CategoriesSerializer,
    GenresSerializer,
    TitleGetSerializer,
    TitlePostPatchSerializer,
    UserSerializer,
    UserRegistrationSerializer,
    NewUserRegistrationSerializer,
    TokenSerializer
)
from .permissions import IsOwnerOrReadOnly, UserIsAdmin
from .filters import TitleFilters


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = LimitOffsetPagination


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    pagination_class = LimitOffsetPagination


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlePostPatchSerializer
    permission_classes = ()
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilters

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializer
        return TitlePostPatchSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(
            Titles,
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Titles,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


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
