from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, filters, permissions
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Titles, Review, User, Categories, Genres, Titles
from .serializers import (
    ReviewSerializer,
    CommentSerializer,
    UserSerializer,
    CategoriesSerializer,
    GenresSerializer,
    TitleGetSerializer,
    TitlePostPatchSerializer,
    NewUserRegistrationSerializer
)
from .permissions import IsOwnerOrReadOnly
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
