from tokenize import TokenError

from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone_number', 'status']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validate_data):
        user = Profile.objects.create_user(**validate_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {'username': instance.username,
                     'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }

class LoginSerializer(serializers.Serializer):
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
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance. username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)

    def validate(self, data):
        refresh_token = data.get('refresh')
        try:
            token = RefreshToken(refresh_token)
            return data
        except TokenError:
            raise serializers.ValidationError({'detail': 'Недействительный токен.'})

    def save(self):
        refresh_token = self.validated_data['refresh']
        token = RefreshToken(refresh_token)
        token.blacklist()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class ProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name']


class CountrySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country_name']


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['director_name']


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['actor_name']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre_name']


class MovieListSerializer(serializers.ModelSerializer):
    year = serializers.DateField(format='%Y')
    country = CountrySerializer(many=True)
    genre = GenreSerializer(many=True)
    class Meta:
        model = Movie
        fields = ['id', 'movie_image', 'movie_name', 'year', 'country', 'genre', 'status_movie']


class MovieLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieLanguage
        fields = ['language', 'video']


class MomentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moments
        fields = ['movie_moment']


class RatingSerializer(serializers.ModelSerializer):
    user = ProfileSimpleSerializer()
    created_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M')

    class Meta:
        model = Rating
        fields = ['user', 'parent', 'text', 'stars', 'created_date']


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class FavoriteMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteMovie
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'


class CountryDetailSerializer(serializers.ModelSerializer):
    countries = MovieListSerializer(read_only=True, many=True)

    class Meta:
        model = Country
        fields = ['country_name', 'countries']


class DirectorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['director_name']


class ActorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['actor_name']


class GenreDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre_name']


class MovieDetailSerializer(serializers.ModelSerializer):
    year = serializers.DateField(format='%d-%m-%Y')
    country = CountrySerializer(many=True)
    genre = GenreSerializer(many=True)
    director = DirectorSerializer(many=True)
    actor = ActorSerializer(many=True)
    languages = MovieLanguageSerializer(many=True, read_only=True)
    moments = MomentsSerializer(many=True, read_only=True)
    ratings = RatingSerializer(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['movie_image', 'movie_name', 'year', 'country', 'director', 'genre',
                  'types', 'movie_trailer',  'movie_time', 'actor', 'descriptions', 'status_movie',
                  'languages', 'moments', 'ratings', 'avg_rating', 'count_people']


    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()