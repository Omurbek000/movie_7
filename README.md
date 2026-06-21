<div align="center">

# 🎬 Movie Platform API

**Полнофункциональный REST API для платформы фильмов**

---

[![Django](https://img.shields.io/badge/Django-5.2.5-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16.1-A30000?style=for-the-badge&logo=python&logoColor=white)](https://www.django-rest-framework.org/)
[![JWT](https://img.shields.io/badge/JWT-SimpleJWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://django-rest-framework-simplejwt.readthedocs.io/)
[![Swagger](https://img.shields.io/badge/Swagger-UI-85EA2D?style=for-the-badge&logo=openapiinitiative&logoColor=black)](http://localhost:8000/en/docs/)

[![Tests](https://img.shields.io/badge/Tests-45%20✅-44CC11?style=for-the-badge)](#-тесты)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](#)

</div>

---

## 📋 Содержание

- [🚀 Возможности](#-возможности)
- [⚡ Быстрый старт](#-быстрый-старт)
- [📡 API Эндпоинты](#-api-эндпоинты)
- [🔐 Аутентификация](#-аутентификация)
- [🌍 Переводы](#-переводы)
- [🔍 Фильтрация и поиск](#-фильтрация-и-поиск)
- [🧪 Тесты](#-тесты)
- [📁 Структура проекта](#-структура-проекта)

---

## 🚀 Возможности

| Функция | Описание |
|---------|----------|
| 🔑 **JWT Аутентификация** | Регистрация, вход, выход, blacklist токенов |
| 🎭 **Соцсети** | Google, GitHub через django-allauth |
| 🌍 **Мультиязычность** | 3 языка: English, Русский, Кыргызча |
| 📄 **Swagger Docs** | Автоматическая документация API |
| 🔍 **Фильтрация** | По жанру, году, стране, режиссёру, актёру |
| 📖 **Поиск** | По названию фильма, описанию, имени режиссёра/актёра |
| 📑 **Пагинация** | Настраиваемая пагинация списков |
| ⭐ **Рейтинги** | Оценки от 1 до 10 с комментариями |
| ❤️ **Избранное** | Персональные списки избранных фильмов |
| 📊 **История** | Отслеживание просмотренных фильмов |
| 🛡️ **Permissions** | Pro/Simple статусы с ограничением контента |
| 🎨 **Admin** | Полная админ-панель с инлайнами |

---

## ⚡ Быстрый старт

### 1. Клонирование и установка

```bash
git clone https://github.com/yourusername/movie_7.git
cd movie_7/my_project

# Создание виртуального окружения
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# Установка зависимостей
pip install -r ../requirements.txt
```

### 2. Настройка окружения

```bash
# Создайте файл .env в папке my_project/
echo SECRET_KEY=your-secret-key-here > .env
echo DEBUG=True >> .env
```

### 3. Запуск

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 4. Откройте

| Страница | URL |
|----------|-----|
| 🎬 API (EN) | http://localhost:8000/en/movie/ |
| 📄 Swagger | http://localhost:8000/en/docs/ |
| 🎛️ Admin | http://localhost:8000/en/admin/ |

---

## 📡 API Эндпоинты

### Аутентификация

| Метод | URL | Описание | Авторизация |
|-------|-----|----------|-------------|
| `POST` | `/en/register/` | Регистрация | ❌ |
| `POST` | `/en/login/` | Вход | ❌ |
| `POST` | `/en/logout/` | Выход | ✅ |

### Фильмы

| Метод | URL | Описание | Авторизация |
|-------|-----|----------|-------------|
| `GET` | `/en/movie/` | Список фильмов | ❌ |
| `GET` | `/en/movie/{id}/` | Детали фильма | ❌ |

### Актёры и Режиссёры

| Метод | URL | Описание | Авторизация |
|-------|-----|----------|-------------|
| `GET` | `/en/actor/` | Список актёров | ❌ |
| `POST` | `/en/actor/` | Создать актёра | ✅ |
| `GET` | `/en/director/` | Список режиссёров | ❌ |
| `POST` | `/en/director/` | Создать режиссёра | ✅ |

### Справочники

| Метод | URL | Описание |
|-------|-----|----------|
| `GET` | `/en/genre/` | Жанры |
| `GET` | `/en/country/` | Страны |
| `GET` | `/en/country/{id}/` | Страна + фильмы |

### Пользователь

| Метод | URL | Описание | Авторизация |
|-------|-----|----------|-------------|
| `GET` | `/en/user/{id}/` | Мой профиль | ✅ |
| `PATCH` | `/en/user/{id}/` | Обновить профиль | ✅ |
| `POST` | `/en/rating/` | Оставить отзыв | ✅ |
| `POST` | `/en/favorite/` | Добавить в избранное | ✅ |
| `GET` | `/en/history/` | История просмотров | ✅ |

---

## 🔐 Аутентификация

### Регистрация

```bash
curl -X POST http://localhost:8000/en/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user1",
    "email": "user@example.com",
    "password": "strongpass123",
    "first_name": "Иван",
    "last_name": "Петров"
  }'
```

**Ответ:**
```json
{
  "user": {
    "id": 1,
    "username": "user1",
    "email": "user@example.com"
  },
  "access": "eyJhbGciOiJIUzI1NiIs...",
  "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

### Использование токена

```bash
curl http://localhost:8000/en/movie/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

---

## 🌍 Переводы

API поддерживает **3 языка** через URL-префикс:

| Язык | Префикс | Пример |
|------|---------|--------|
| 🇬🇧 English | `/en/` | `/en/movie/` |
| 🇷🇺 Русский | `/ru/` | `/ru/movie/` |
| 🇰🇬 Кыргызча | `/ky/` | `/ky/movie/` |

### Что переводится

| Модель | Поля |
|--------|------|
| 🎬 Movie | `movie_name`, `descriptions` |
| 🎭 Director | `director_name`, `director_bio` |
| 🎬 Actor | `actor_name`, `actor_bio` |
| 🎵 Genre | `genre_name` |
| 🌍 Country | `country_name` |

### Пример

```bash
# English
GET /en/movie/1/
→ "movie_name": "Interstellar"

# Русский
GET /ru/movie/1/
→ "movie_name": "Интерстеллар"

# Кыргызча
GET /ky/movie/1/
→ "movie_name": "Интерстеллар"
```

---

## 🔍 Фильтрация и поиск

### Фильтры фильмов

| Параметр | Тип | Описание | Пример |
|----------|-----|----------|--------|
| `genre` | ID | Фильтр по жанру | `?genre=1` |
| `country` | ID | Фильтр по стране | `?country=1` |
| `director` | ID | Фильтр по режиссёру | `?director=2` |
| `actor` | ID | Фильтр по актёру | `?actor=3` |
| `year__gt` | Число | Год больше | `?year__gt=2020` |
| `year__lt` | Число | Год меньше | `?year__lt=2025` |
| `year_exact` | Число | Точный год | `?year_exact=2024` |
| `movie_time__gt` | Число | Длительность > мин | `?movie_time__gt=90` |

### Фильтры актёров

| Параметр | Описание | Пример |
|----------|----------|--------|
| `age_gte` | Возраст от | `?age_gte=30` |
| `age_lte` | Возраст до | `?age_lte=50` |

### Поиск

| Параметр | Описание | Пример |
|----------|----------|--------|
| `search` | Поиск по тексту | `?search=Интерстеллар` |

### Сортировка

| Параметр | Описание | Пример |
|----------|----------|--------|
| `ordering` | Сортировка | `?ordering=year` |
| `ordering` | По убыванию | `?ordering=-movie_time` |

### Примеры запросов

```bash
# Боевики после 2020 года
GET /en/movie/?genre=1&year__gt=2020

# Фильмы Нолана
GET /en/movie/?search=Нолан

# Актёры 30-50 лет
GET /en/actor/?age_gte=30&age_lte=50

# Длинные фильмы (>2 часов), отсортированные по году
GET /en/movie/?movie_time__gt=120&ordering=-year
```

---

## 🧪 Тесты

```bash
python manage.py test movie --verbosity=2
```

### Покрытие

| Класс | Тесты | Описание |
|-------|-------|----------|
| `ModelStrTest` | 12 | `__str__` методы моделей |
| `MovieRatingTest` | 3 | Подсчёт рейтинга |
| `RegisterTest` | 2 | Регистрация пользователя |
| `LoginTest` | 3 | Вход в систему |
| `LogoutTest` | 3 | Выход из системы |
| `MovieAPITest` | 5 | CRUD фильмов, поиск, фильтры |
| `CountryAPITest` | 2 | API стран |
| `RatingAPITest` | 3 | Создание рейтингов |
| `FavoriteAPITest` | 3 | Избранное |
| `HistoryAPITest` | 2 | История просмотров |
| `ProfileAPITest` | 2 | Профиль пользователя |
| `DirectorActorGenreAPITest` | 5 | CRUD справочников |

**Итого: 45 тестов ✅**

---

## 📁 Структура проекта

```
movie_7/
├── .gitignore
├── requirements.txt
├── README.md
└── my_project/
    ├── manage.py
    ├── .env                      # Секреты (не коммитить!)
    ├── my_project/
    │   ├── settings.py           # Настройки Django
    │   ├── urls.py               # Корневые URL
    │   ├── wsgi.py
    │   └── asgi.py
    └── movie/                    # Основное приложение
        ├── models.py             # Модели: Profile, Movie, Actor...
        ├── serializers.py        # Сериализаторы API
        ├── views.py              # API Views
        ├── urls.py               # URL-маршруты
        ├── admin.py              # Админ-панель
        ├── filter.py             # Фильтры DjangoFilter
        ├── paginations.py        # Пагинация
        ├── permissions.py        # Кастомные права
        ├── translation.py        # Переводы (en/ru/ky)
        ├── tests.py              # 45 тестов
        ├── apps.py
        └── migrations/
            ├── 0001_initial.py
            └── 0002_*_ky.py     # Миграция для кыргызского
```

---

## 🛠️ Технологии

| Технология | Версия | Назначение |
|------------|--------|------------|
| Python | 3.12 | Язык программирования |
| Django | 5.2.5 | Web-фреймворк |
| DRF | 3.16.1 | REST API |
| SimpleJWT | 5.5.1 | JWT-аутентификация |
| django-allauth | 65.10.0 | Соцсети (Google, GitHub) |
| django-filter | 25.1 | Фильтрация API |
| modeltranslation | 0.19.16 | Мультиязычность |
| drf-yasg | 1.21.10 | Swagger-документация |
| Pillow | 11.3.0 | Загрузка изображений |

---

<div align="center">

**Сделано с ❤️ для Movie Platform**

[Наверх ↑](#-movie-platform-api)

</div>
