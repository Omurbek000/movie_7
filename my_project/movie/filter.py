from .models import Movie
from django_filters.rest_framework import FilterSet


class MovieFilter(FilterSet):
    class Meta:
        model = Movie
        fields = {
            'country': ['exact'],
            'genre': ['exact'],
            'director': ['exact'],
            'actor': ['exact'],
            'year': ['gt', 'lt'],
            'movie_time': ['gt', 'lt']
        }