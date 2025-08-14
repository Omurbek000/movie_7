from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'user', ProfileViewSet, basename='users')
router.register(r'director', DirectorViewSet, basename='directories')
router.register(r'actor', ActorViewSet, basename='actors')
router.register(r'genre', GenreViewSet, basename='genres')
router.register(r'movie_language', MovieLanguageViewSet, basename='movie-languages')
router.register(r'moment', MomentsViewSet, basename='moments')
router.register(r'rating', RatingViewSet, basename='ratings')
router.register(r'favorite', FavoriteViewSet, basename='favorites')
router.register(r'favorite_movie', FavoriteMovieViewSet, basename='favorite-movie')
router.register(r'history', HistoryViewSet, basename='histories')

urlpatterns = [
    path('', include(router.urls)),
    path('register', RegisterView.as_view(), name='register'),
    path('login', CustomLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

    path('movie/', MovieListAPIView.as_view(), name='movie-list'),
    path('movie/<int:pk>/', MovieDetailAPIView.as_view(), name='movie-detail'),

    path('country/', CountryAPIView.as_view(), name='country-list'),
    path('country/<int:pk>/', CountryDetailAPIView.as_view(), name='country-detail'),
]
