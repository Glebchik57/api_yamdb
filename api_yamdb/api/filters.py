from django_filters import rest_framework as filters
from reviews.models import Titles


class TitleFilters(filters.FilterSet):
    category = filters.CharFilter(name='category_slug')
    genre = filters.CharFilter(name='genre_slug')
    year = filters.CharFilter(name='year')

    class Meta:
        model = Titles
        fields = [
            'year',
            'category',
            'genre'
        ]
