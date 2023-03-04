from reviews.models import Categories, Genres, Titles, Review
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TitleFilters
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from .serializers import CategoriesSerializer, GenresSerializer, TitleGetSerializer, TitlePostPatchSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = LimitOffsetPagination


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = CategoriesSerializer
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
