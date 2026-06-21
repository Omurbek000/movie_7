from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate
from .models import (Profile, Country, Director, Actor, Genre, Movie,
                     MovieLanguage, Moments, Rating, Favorite, FavoriteMovie, History)


# ==================== АУТЕНТИФИКАЦИЯ ====================

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя. Возвращает JWT-токены после создания"""
    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone_number', 'status']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Profile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'id': instance.id,
                'username': instance.username,
                'email': instance.email,
                'first_name': instance.first_name,
                'last_name': instance.last_name,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }


class LoginSerializer(serializers.Serializer):
    """Сериализатор входа: проверяет username/password, возвращает JWT"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = Profile.objects.filter(username=username).first()
        if not user:
            raise serializers.ValidationError("Пользователь с таким username не найден")
        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError("Неверные учетные данные")
        return {'user': user}

    def to_representation(self, instance):
        user = instance['user']
        refresh = RefreshToken.for_user(user)
        return {
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'status': user.status,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LogoutSerializer(serializers.Serializer):
    """Сериализатор выхода: блокирует refresh-токен"""
    refresh = serializers.CharField(required=True)

    def validate(self, data):
        try:
            token = RefreshToken(data['refresh'])
            return data
        except TokenError:
            raise serializers.ValidationError({'detail': 'Недействительный токен.'})

    def save(self):
        token = RefreshToken(self.validated_data['refresh'])
        token.blacklist()


# ==================== ПРОФИЛЬ ====================

class ProfileSerializer(serializers.ModelSerializer):
    """Полный профиль пользователя (CRUD)"""
    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'phone_number', 'age', 'avatar', 'status', 'data_registered']
        read_only_fields = ['id', 'data_registered']


class ProfileSimpleSerializer(serializers.ModelSerializer):
    """Краткая информация о пользователе (для вложений в Rating)"""
    class Meta:
        model = Profile
        fields = ['id', 'first_name', 'last_name']


# ==================== СПРАВОЧНИКИ ====================

class CountrySerializer(serializers.ModelSerializer):
    """Страна (без вложенных фильмов)"""
    class Meta:
        model = Country
        fields = ['id', 'country_name']


class DirectorSerializer(serializers.ModelSerializer):
    """Режиссёр"""
    class Meta:
        model = Director
        fields = ['id', 'director_name', 'director_bio', 'director_age', 'director_image']


class ActorSerializer(serializers.ModelSerializer):
    """Актёр"""
    class Meta:
        model = Actor
        fields = ['id', 'actor_name', 'actor_bio', 'actor_age', 'actor_image']


class GenreSerializer(serializers.ModelSerializer):
    """Жанр"""
    class Meta:
        model = Genre
        fields = ['id', 'genre_name']


# ==================== РЕЙТИНГ (до фильмов, т.к. MovieDetailSerializer ссылается) ====================

class RatingSerializer(serializers.ModelSerializer):
    """Отзыв/оценка фильма с вложенными комментариями"""
    user = ProfileSimpleSerializer(read_only=True)
    created_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M', read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'user', 'parent', 'movie', 'text', 'stars', 'created_date']
        read_only_fields = ['id', 'user', 'created_date']

    def validate_stars(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError("Оценка должна быть от 1 до 10")
        return value


# ==================== ФИЛЬМЫ ====================

class MovieLanguageSerializer(serializers.ModelSerializer):
    """Язык и видеофайл фильма"""
    class Meta:
        model = MovieLanguage
        fields = ['id', 'language', 'video']


class MomentsSerializer(serializers.ModelSerializer):
    """Кадр/скриншот из фильма"""
    class Meta:
        model = Moments
        fields = ['id', 'movie_moment']


class MovieListSerializer(serializers.ModelSerializer):
    """Список фильмов (краткая карточка для ленты)"""
    year = serializers.DateField(format='%Y')
    country = CountrySerializer(many=True, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'movie_image', 'movie_name', 'year', 'country', 'genre', 'status_movie']


class MovieDetailSerializer(serializers.ModelSerializer):
    """Детальная информация о фильме со всеми связями"""
    year = serializers.DateField(format='%d-%m-%Y')
    country = CountrySerializer(many=True, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    director = DirectorSerializer(many=True, read_only=True)
    actor = ActorSerializer(many=True, read_only=True)
    languages = MovieLanguageSerializer(many=True, read_only=True)
    moments = MomentsSerializer(many=True, read_only=True)
    ratings = RatingSerializer(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'movie_image', 'movie_name', 'year', 'country', 'director', 'genre',
                  'types', 'movie_trailer', 'movie_time', 'actor', 'descriptions', 'status_movie',
                  'languages', 'moments', 'ratings', 'avg_rating', 'count_people']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()


# ==================== СТРАНА (с фильмами) ====================

class CountryDetailSerializer(serializers.ModelSerializer):
    """Страна с вложенными фильмами"""
    countries = MovieListSerializer(read_only=True, many=True)

    class Meta:
        model = Country
        fields = ['id', 'country_name', 'countries']


# ==================== ИЗБРАННОЕ ====================

class FavoriteSerializer(serializers.ModelSerializer):
    """Списки избранного пользователя"""
    class Meta:
        model = Favorite
        fields = ['id', 'user']
        read_only_fields = ['id']


class FavoriteMovieSerializer(serializers.ModelSerializer):
    """Фильм в избранном"""
    class Meta:
        model = FavoriteMovie
        fields = ['id', 'favorite', 'movie']
        read_only_fields = ['id']


# ==================== ИСТОРИЯ ====================

class HistorySerializer(serializers.ModelSerializer):
    """История просмотров. При чтении — вложенный фильм, при записи — id фильма"""
    movie_detail = MovieListSerializer(source='movie', read_only=True)

    class Meta:
        model = History
        fields = ['id', 'user', 'movie', 'movie_detail', 'viewed_at']
        read_only_fields = ['id', 'user', 'viewed_at']
