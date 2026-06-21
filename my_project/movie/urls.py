"""
URL-маршруты приложения movie.
Все маршруты попадают под i18n-префикс /<lang>/
"""
from django.urls import path, include
from rest_framework import routers
from .views import (RegisterView, CustomLoginView, LogoutView,
                    ProfileViewSet, CountryAPIView, CountryDetailAPIView,
                    DirectorViewSet, ActorViewSet, GenreViewSet,
                    MovieListAPIView, MovieDetailAPIView,
                    MovieLanguageViewSet, MomentsViewSet,
                    RatingViewSet, FavoriteViewSet,
                    FavoriteMovieViewSet, HistoryViewSet)

# Router для ViewSet'ов (автоматические CRUD-маршруты)
router = routers.SimpleRouter()
router.register(r'user', ProfileViewSet, basename='users')
router.register(r'director', DirectorViewSet, basename='directors')
router.register(r'actor', ActorViewSet, basename='actors')
router.register(r'genre', GenreViewSet, basename='genres')
router.register(r'movie_language', MovieLanguageViewSet, basename='movie-languages')
router.register(r'moment', MomentsViewSet, basename='moments')
router.register(r'rating', RatingViewSet, basename='ratings')
router.register(r'favorite', FavoriteViewSet, basename='favorites')
router.register(r'favorite_movie', FavoriteMovieViewSet, basename='favorite-movies')
router.register(r'history', HistoryViewSet, basename='histories')

urlpatterns = [
    # Аутентификация
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Фильмы
    path('movie/', MovieListAPIView.as_view(), name='movie-list'),
    path('movie/<int:pk>/', MovieDetailAPIView.as_view(), name='movie-detail'),

    # Страны
    path('country/', CountryAPIView.as_view(), name='country-list'),
    path('country/<int:pk>/', CountryDetailAPIView.as_view(), name='country-detail'),

    # ViewSet'ы (user, director, actor, genre, rating, favorite, history...)
    path('', include(router.urls)),
]
