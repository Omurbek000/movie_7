from rest_framework import viewsets, generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import (Profile, Country, Director, Actor, Genre, Movie,
                     MovieLanguage, Moments, Rating, Favorite, FavoriteMovie, History)
from .serializers import (UserSerializer, LoginSerializer, ProfileSerializer,
                          CountrySerializer, CountryDetailSerializer,
                          DirectorSerializer, ActorSerializer, GenreSerializer,
                          MovieListSerializer, MovieDetailSerializer,
                          MovieLanguageSerializer, MomentsSerializer,
                          RatingSerializer, FavoriteSerializer,
                          FavoriteMovieSerializer, HistorySerializer)
from .filter import MovieFilter, ActorFilter
from .paginations import MoviePagination
from .permissions import CheckStatus, IsOwnerOrReadOnly


# ==================== АУТЕНТИФИКАЦИЯ ====================

class RegisterView(generics.CreateAPIView):
    """POST /register — регистрация нового пользователя, возвращает JWT"""
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    """POST /login — вход по username/password, возвращает access + refresh токены"""
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({'detail': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """POST /logout — blacklist refresh-токена (выход из системы)"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'detail': 'Refresh токен не предоставлен.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Вы успешно вышли.'}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({'detail': 'Недействительный токен.'},
                            status=status.HTTP_400_BAD_REQUEST)


# ==================== ПРОФИЛЬ ====================

class ProfileViewSet(viewsets.ModelViewSet):
    """CRUD профиля текущего пользователя. Другие пользователи не видны."""
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(id=self.request.user.id)


# ==================== СПРАВОЧНИКИ (read-only для всех) ====================

class CountryAPIView(generics.ListAPIView):
    """GET /country/ — список всех стран"""
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [permissions.AllowAny]


class CountryDetailAPIView(generics.RetrieveAPIView):
    """GET /country/{id}/ — детали страны со списком фильмов"""
    queryset = Country.objects.all()
    serializer_class = CountryDetailSerializer
    permission_classes = [permissions.AllowAny]


class DirectorViewSet(viewsets.ModelViewSet):
    """CRUD режиссёров (только аутентифицированные для записи)"""
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ActorViewSet(viewsets.ModelViewSet):
    """CRUD актёров с поиском и фильтрацией по возрасту"""
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = MoviePagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ActorFilter
    search_fields = ['actor_name']


class GenreViewSet(viewsets.ModelViewSet):
    """CRUD жанров (только аутентифицированные для записи)"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ==================== ФИЛЬМЫ ====================

class MovieListAPIView(generics.ListAPIView):
    """GET /movie/ — список фильмов с фильтрацией, поиском, сортировкой, пагинацией"""
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['movie_name', 'descriptions', 'director__director_name', 'actor__actor_name']
    ordering_fields = ['year', 'movie_time']
    filterset_class = MovieFilter
    pagination_class = MoviePagination
    permission_classes = [permissions.AllowAny]


class MovieDetailAPIView(generics.RetrieveAPIView):
    """GET /movie/{id}/ — детальная информация о фильме"""
    queryset = Movie.objects.all()
    serializer_class = MovieDetailSerializer
    permission_classes = [permissions.AllowAny]


class MovieLanguageViewSet(viewsets.ModelViewSet):
    """CRUD языков/видео фильма"""
    queryset = MovieLanguage.objects.all()
    serializer_class = MovieLanguageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MomentsViewSet(viewsets.ModelViewSet):
    """CRUD кадров фильма"""
    queryset = Moments.objects.all()
    serializer_class = MomentsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ==================== РЕЙТИНГ ====================

class RatingViewSet(viewsets.ModelViewSet):
    """CRUD отзывов/оценок. Только аутентифицированные. Пользователь видит/меняет свои."""
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ==================== ИЗБРАННОЕ ====================

class FavoriteViewSet(viewsets.ModelViewSet):
    """Списки избранного. Только свои."""
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteMovieViewSet(viewsets.ModelViewSet):
    """Фильмы в избранном. CRUD."""
    serializer_class = FavoriteMovieSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoriteMovie.objects.filter(favorite__user=self.request.user)


# ==================== ИСТОРИЯ ====================

class HistoryViewSet(viewsets.ModelViewSet):
    """История просмотров. Только свои записи."""
    serializer_class = HistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return History.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
