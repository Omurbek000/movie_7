from .models import Movie, Actor
from django_filters.rest_framework import FilterSet, filters


class MovieFilter(FilterSet):
    """Фильтрация фильмов: страна, жанр, режиссёр, актёр, год, длительность"""
    year_exact = filters.NumberFilter(field_name='year', lookup_expr='year')
    year_gte = filters.NumberFilter(field_name='year', lookup_expr='year__gte')
    year_lte = filters.NumberFilter(field_name='year', lookup_expr='year__lte')

    class Meta:
        model = Movie
        fields = {
            'country': ['exact'],
            'genre': ['exact'],
            'director': ['exact'],
            'actor': ['exact'],
            'year': ['gt', 'lt'],
            'movie_time': ['gt', 'lt'],
        }


class ActorFilter(FilterSet):
    """Фильтрация актёров: возраст"""
    age_gte = filters.NumberFilter(field_name='actor_age', lookup_expr='gte')
    age_lte = filters.NumberFilter(field_name='actor_age', lookup_expr='lte')

    class Meta:
        model = Actor
        fields = ['actor_age']