from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date

from .models import (Profile, Country, Director, Actor, Genre, Movie,
                     MovieLanguage, Moments, Rating, Favorite, FavoriteMovie, History)

Profile = get_user_model()

ROOT_URLCONF = 'movie.tests_i18n_urls'


# ==================== ТЕСТЫ МОДЕЛЕЙ ====================

class ModelStrTest(TestCase):
    """Тест __str__ методов моделей"""

    def setUp(self):
        self.profile = Profile.objects.create_user(
            username='testuser', password='testpass123',
            first_name='Иван', last_name='Петров'
        )
        self.country = Country.objects.create(country_name='Россия')
        self.director = Director.objects.create(
            director_name='Таранов', director_bio='Био', director_age=45
        )
        self.actor = Actor.objects.create(
            actor_name='Сидоров', actor_bio='Био', actor_age=30
        )
        self.genre = Genre.objects.create(genre_name='Комедия')
        self.movie = Movie.objects.create(
            movie_name='Тест Фильм', year=date(2024, 1, 1),
            movie_time=120, descriptions='Описание',
            movie_trailer='https://youtube.com/watch?v=123',
            movie_image='test.jpg'
        )
        self.movie.country.add(self.country)
        self.movie.director.add(self.director)
        self.movie.actor.add(self.actor)
        self.movie.genre.add(self.genre)

    def test_profile_str(self):
        self.assertEqual(str(self.profile), 'Иван Петров')

    def test_country_str(self):
        self.assertEqual(str(self.country), 'Россия')

    def test_director_str(self):
        self.assertEqual(str(self.director), 'Таранов')

    def test_actor_str(self):
        self.assertEqual(str(self.actor), 'Сидоров')

    def test_genre_str(self):
        self.assertEqual(str(self.genre), 'Комедия')

    def test_movie_str(self):
        self.assertEqual(str(self.movie), 'Тест Фильм')

    def test_movie_language_str(self):
        lang = MovieLanguage.objects.create(
            language='Русский', movie=self.movie
        )
        self.assertIn('Русский', str(lang))
        self.assertIn('Тест Фильм', str(lang))

    def test_moments_str(self):
        moment = Moments.objects.create(movie=self.movie)
        self.assertIn('Тест Фильм', str(moment))

    def test_rating_str(self):
        rating = Rating.objects.create(
            user=self.profile, movie=self.movie,
            stars=8, text='Отличный фильм'
        )
        self.assertIn('Иван', str(rating))
        self.assertIn('Тест Фильм', str(rating))

    def test_favorite_str(self):
        fav = Favorite.objects.create(user=self.profile)
        self.assertEqual(str(fav), 'Иван Петров')

    def test_favorite_movie_str(self):
        fav = Favorite.objects.create(user=self.profile)
        fav_movie = FavoriteMovie.objects.create(favorite=fav, movie=self.movie)
        self.assertIn('Тест Фильм', str(fav_movie))

    def test_history_str(self):
        history = History.objects.create(user=self.profile, movie=self.movie)
        self.assertIn('Иван', str(history))
        self.assertIn('Тест Фильм', str(history))


class MovieRatingTest(TestCase):
    """Тесты методов рейтинга фильма"""

    def setUp(self):
        self.profile = Profile.objects.create_user(
            username='user1', password='pass123'
        )
        self.movie = Movie.objects.create(
            movie_name='Фильм', year=date(2024, 1, 1),
            movie_time=90, descriptions='Описание',
            movie_trailer='https://youtube.com/watch?v=1',
            movie_image='test.jpg'
        )

    def test_get_avg_rating_no_ratings(self):
        self.assertEqual(self.movie.get_avg_rating(), 0)

    def test_get_avg_rating_with_ratings(self):
        Rating.objects.create(user=self.profile, movie=self.movie, stars=8, text='Хорош')
        Rating.objects.create(user=self.profile, movie=self.movie, stars=6, text='Норм')
        avg = self.movie.get_avg_rating()
        self.assertEqual(avg, 7.0)

    def test_get_count_people(self):
        self.assertEqual(self.movie.get_count_people(), 0)
        Rating.objects.create(user=self.profile, movie=self.movie, stars=5, text='Ок')
        self.assertEqual(self.movie.get_count_people(), 1)


# ==================== ТЕСТЫ API ====================
# URLs используют i18n_patterns, поэтому все URL-ы с префиксом /en/

@override_settings(ROOT_URLCONF=ROOT_URLCONF)
class RegisterTest(APITestCase):
    """Тест регистрации пользователя"""

    def setUp(self):
        self.data = {
            'username': 'newuser',
            'email': 'new@test.com',
            'password': 'strongpass123',
            'first_name': 'Новый',
            'last_name': 'Пользователь',
        }

    def test_register_success(self):
        response = self.client.post('/en/register/', self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['username'], 'newuser')

    def test_register_duplicate_username(self):
        Profile.objects.create_user(username='newuser', password='pass123')
        response = self.client.post('/en/register/', self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@override_settings(ROOT_URLCONF=ROOT_URLCONF)
class LoginTest(APITestCase):
    """Тест входа в систему"""

    def setUp(self):
        self.user = Profile.objects.create_user(
            username='loginuser', password='loginpass123'
        )
        self.data = {'username': 'loginuser', 'password': 'loginpass123'}

    def test_login_success(self):
        response = self.client.post('/en/login/', self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['username'], 'loginuser')

    def test_login_wrong_password(self):
        response = self.client.post('/en/login/', {'username': 'loginuser', 'password': 'wrong'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_nonexistent_user(self):
        response = self.client.post('/en/login/', {'username': 'nobody', 'password': 'pass'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


@override_settings(ROOT_URLCONF=ROOT_URLCONF)
class LogoutTest(APITestCase):
    """Тест выхода из системы"""

    def setUp(self):
        self.user = Profile.objects.create_user(
            username='logoutuser', password='logoutpass123'
        )
        refresh = RefreshToken.for_user(self.user)
        self.refresh_token = str(refresh)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_logout_success(self):
        response = self.client.post('/en/logout/', {'refresh': self.refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_no_token(self):
        response = self.client.post('/en/logout/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_invalid_token(self):
        response = self.client.post('/en/logout/', {'refresh': 'invalid_token'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@override_settings(ROOT_URLCONF=ROOT_URLCONF)
class MovieAPITest(APITestCase):
    """Тесты API фильмов"""

    def setUp(self):
        self.user = Profile.objects.create_user(
            username='moviefan', password='moviepass123'
        )
        self.country = Country.objects.create(country_name='США')
        self.genre = Genre.objects.create(genre_name='Боевик')
        self.director = Director.objects.create(
            director_name='Нолан', director_bio='Био', director_age=55
        )
        self.actor = Actor.objects.create(
            actor_name='ДиКаприо', actor_bio='Био', actor_age=50
        )
        self.movie = Movie.objects.create(
            movie_name='Интерстеллар', year=date(2014, 11, 7),
            movie_time=169, descriptions='Космос',
            movie_trailer='https://youtube.com/watch?v=abc',
            movie_image='interstellar.jpg', status_movie='simple'
        )
        self.movie.country.add(self.country)
        self.movie.genre.add(self.genre)
        self.movie.director.add(self.director)
        self.movie.actor.add(self.actor)

    def test_movie_list(self):
        response = self.client.get('/en/movie/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_movie_detail(self):
        response = self.client.get(f'/en/movie/{self.movie.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['movie_name'], 'Интерстеллар')

    def test_movie_search(self):
        response = self.client.get('/en/movie/?search=Интерстеллар')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_movie_filter_by_genre(self):
        response = self.client.get(f'/en/movie/?genre={self.genre.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_movie_filter_by_country(self):
        response = self.client.get(f'/en/movie/?country={self.country.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


@override_settings(ROOT_URLCONF=ROOT_URLCONF)
class CountryAPITest(APITestCase):
    """Тесты API стран"""

    def setUp(self):
        self.country = Country.objects.create(country_name='Франция')
        self.movie = Movie.objects.create(
            movie_name='Французский фильм', year=date(2020, 1, 1),
            movie_time=100, descriptions='Описание',
            movie_trailer='https://youtube.com/watch?v=1',
            movie_image='fr.jpg'
        )
        self.movie.country.add(self.country)

    def test_country_list(self):
        response = self.client.get('/en/country/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_country_detail(self):
        response = self.client.get(f'/en/country/{self.country.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('countries', response.data)


@override_settings(ROOT_URLCONF=ROOT_URLCONF)
class RatingAPITest(APITestCase):
    """Тесты API рейтингов"""

    def setUp(self):
        self.user = Profile.objects.create_user(
            username='rater', password='ratepass123'
        )
        self.movie = Movie.objects.create(
            movie_name='Фильм для рейтинга', year=date(2023, 1, 1),
            movie_time=120, descriptions='Описание',
            movie_trailer='https://youtube.com/watch?v=1',
            movie_image='rate.jpg'
        )
        self.refresh = RefreshToken.for_user(self.user)

    def test_create_rating_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        response = self.client.post('/en/rating/', {
            'movie': self.movie.id,
            'stars': 9,
            'text': 'Шедевр!'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rating.objects.count(), 1)

    def test_create_rating_unauthenticated(self):
        response = self.client.post('/en/rating/', {
            'movie': self.movie.id,
            'stars': 9,
            'text': 'Шедевр!'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_rating_stars_validation(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        response = self.client.post('/en/rating/', {
            'movie': self.movie.id,
            'stars': 11,
            'text': 'Слишком много'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@override_settings(ROOT_URLCONF=ROOT_URLCONF)
class FavoriteAPITest(APITestCase):
    """Тесты API избранного"""

    def setUp(self):
        self.user = Profile.objects.create_user(
            username='favuser', password='favpass123'
        )
        self.movie = Movie.objects.create(
            movie_name='Любимый фильм', year=date(2022, 1, 1),
            movie_time=100, descriptions='Описание',
            movie_trailer='https://youtube.com/watch?v=1',
            movie_image='fav.jpg'
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')

    def test_create_favorite(self):
        response = self.client.post('/en/favorite/', {'user': self.user.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_movie_to_favorite(self):
        fav = Favorite.objects.create(user=self.user)
        response = self.client.post('/en/favorite_movie/', {
            'favorite': fav.id,
            'movie': self.movie.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FavoriteMovie.objects.count(), 1)

    def test_favorite_only_own(self):
        other_user = Profile.objects.create_user(
            username='other', password='other123'
        )
        Favorite.objects.create(user=other_user)
        response = self.client.get('/en/favorite/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)


@override_settings(ROOT_URLCONF=ROOT_URLCONF)
class HistoryAPITest(APITestCase):
    """Тесты API истории просмотров"""

    def setUp(self):
        self.user = Profile.objects.create_user(
            username='historyuser', password='history123'
        )
        self.movie = Movie.objects.create(
            movie_name='Просмотренный фильм', year=date(2021, 1, 1),
            movie_time=90, descriptions='Описание',
            movie_trailer='https://youtube.com/watch?v=1',
            movie_image='hist.jpg'
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')

    def test_create_history(self):
        response = self.client.post('/en/history/', {
            'user': self.user.id,
            'movie': self.movie.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_history_only_own(self):
        other_user = Profile.objects.create_user(
            username='other2', password='other2123'
        )
        History.objects.create(user=other_user, movie=self.movie)
        response = self.client.get('/en/history/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)


@override_settings(ROOT_URLCONF=ROOT_URLCONF)
class ProfileAPITest(APITestCase):
    """Тесты API профиля"""

    def setUp(self):
        self.user = Profile.objects.create_user(
            username='profileuser', password='profile123',
            first_name='Тест', last_name='Юзер'
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')

    def test_get_own_profile(self):
        response = self.client.get(f'/en/user/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'profileuser')

    def test_update_own_profile(self):
        response = self.client.patch(f'/en/user/{self.user.id}/', {
            'first_name': 'Обновлённый'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Обновлённый')


@override_settings(ROOT_URLCONF=ROOT_URLCONF)
class DirectorActorGenreAPITest(APITestCase):
    """Тесты API справочников"""

    def setUp(self):
        self.user = Profile.objects.create_user(
            username='creator', password='creator123'
        )
        self.refresh = RefreshToken.for_user(self.user)

    def test_director_create_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        response = self.client.post('/en/director/', {
            'director_name': 'Новый режиссёр',
            'director_bio': 'Биография',
            'director_age': 40
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_director_create_unauthenticated(self):
        response = self.client.post('/en/director/', {
            'director_name': 'Режиссёр',
            'director_bio': 'Био',
            'director_age': 40
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_director_list(self):
        Director.objects.create(
            director_name='Тест', director_bio='Био', director_age=30
        )
        response = self.client.get('/en/director/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_actor_create_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        response = self.client.post('/en/actor/', {
            'actor_name': 'Новый актёр',
            'actor_bio': 'Биография',
            'actor_age': 35
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_genre_create_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        response = self.client.post('/en/genre/', {
            'genre_name': 'Новый жанр'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
