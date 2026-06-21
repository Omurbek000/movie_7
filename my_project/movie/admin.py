from django.contrib import admin
from .models import (Profile, Country, Director, Actor, Genre, Movie,
                     MovieLanguage, Moments, Rating, Favorite, FavoriteMovie, History)
from modeltranslation.admin import TranslationAdmin

# Общий Media для admin с modeltranslation
TRANSLATION_MEDIA = {
    'js': (
        'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js',
        'https://ajax.googleapis.com/ajax/libs/jqueryui/1.13.2/jquery-ui.min.js',
        'modeltranslation/js/tabbed_translation_fields.js',
    ),
    'css': {
        'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
    },
}


# ==================== ИНЛАЙНЫ ====================

class MovieLanguageInline(admin.TabularInline):
    """Языки и видеофайлы фильма"""
    model = MovieLanguage
    extra = 1
    fields = ['language', 'video']


class MovieMomentsInline(admin.TabularInline):
    """Кадры/скриншоты фильма"""
    model = Moments
    extra = 1
    fields = ['movie_moment']


class MovieRatingInline(admin.TabularInline):
    """Рейтинги фильма (только чтение)"""
    model = Rating
    extra = 0
    readonly_fields = ['user', 'stars', 'text', 'created_date']
    fields = ['user', 'stars', 'text', 'created_date']
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


class FavoriteMovieInline(admin.TabularInline):
    """Фильмы в избранном пользователя (для FavoriteAdmin)"""
    model = FavoriteMovie
    extra = 1
    fields = ['movie']


class FavoriteInline(admin.StackedInline):
    """Избранное пользователя (для ProfileAdmin)"""
    model = Favorite
    extra = 0
    can_delete = False
    show_change_link = True


class RatingInline(admin.TabularInline):
    """Отзывы пользователя"""
    model = Rating
    extra = 0
    readonly_fields = ['movie', 'stars', 'text', 'created_date']
    fields = ['movie', 'stars', 'text', 'created_date']
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


# ==================== ФИЛЬМ ====================

@admin.register(Movie)
class MovieAdmin(TranslationAdmin):
    """Управление фильмами с inline-языками, кадрами и рейтингами"""
    list_display = ['movie_name', 'year', 'types', 'status_movie', 'get_avg_rating']
    list_filter = ['status_movie', 'types', 'genre', 'country']
    search_fields = ['movie_name', 'descriptions']
    filter_horizontal = ['country', 'director', 'actor', 'genre']
    inlines = [MovieLanguageInline, MovieMomentsInline, MovieRatingInline]
    readonly_fields = ['get_avg_rating', 'get_count_people']
    fieldsets = (
        (None, {
            'fields': ('movie_name', 'year', 'types', 'status_movie')
        }),
        ('Связи', {
            'fields': ('country', 'director', 'actor', 'genre')
        }),
        ('Контент', {
            'fields': ('descriptions', 'movie_trailer', 'movie_image', 'movie_time')
        }),
        ('Статистика', {
            'fields': ('get_avg_rating', 'get_count_people'),
            'classes': ('collapse',)
        }),
    )

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()
    get_avg_rating.short_description = 'Средний рейтинг'

    def get_count_people(self, obj):
        return obj.get_count_people()
    get_count_people.short_description = 'Кол-во оценок'

    class Media:
        js = TRANSLATION_MEDIA['js']
        css = TRANSLATION_MEDIA['css']


# ==================== СПРАВОЧНИКИ ====================

@admin.register(Country)
class CountryAdmin(TranslationAdmin):
    """Страны"""
    list_display = ['country_name']
    search_fields = ['country_name']
    class Media:
        js = TRANSLATION_MEDIA['js']
        css = TRANSLATION_MEDIA['css']


@admin.register(Genre)
class GenreAdmin(TranslationAdmin):
    """Жанры"""
    list_display = ['genre_name']
    search_fields = ['genre_name']
    class Media:
        js = TRANSLATION_MEDIA['js']
        css = TRANSLATION_MEDIA['css']


@admin.register(Director)
class DirectorAdmin(TranslationAdmin):
    """Режиссёры с inline-фильмами"""
    list_display = ['director_name', 'director_age']
    search_fields = ['director_name']
    list_filter = ['director_age']
    class Media:
        js = TRANSLATION_MEDIA['js']
        css = TRANSLATION_MEDIA['css']


@admin.register(Actor)
class ActorAdmin(TranslationAdmin):
    """Актёры с inline-фильмами"""
    list_display = ['actor_name', 'actor_age']
    search_fields = ['actor_name']
    list_filter = ['actor_age']
    class Media:
        js = TRANSLATION_MEDIA['js']
        css = TRANSLATION_MEDIA['css']


# ==================== ПОЛЬЗОВАТЕЛЬ ====================

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Профиль пользователя с избранным и историей"""
    list_display = ['username', 'email', 'status', 'age', 'data_registered']
    list_filter = ['status', 'data_registered']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    readonly_fields = ['data_registered']
    inlines = [FavoriteInline, RatingInline]


# ==================== РЕЙТИНГ ====================

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Отзывы/оценки"""
    list_display = ['user', 'movie', 'stars', 'created_date']
    list_filter = ['stars', 'created_date']
    search_fields = ['text']
    readonly_fields = ['created_date']
    raw_id_fields = ['user', 'movie', 'parent']


# ==================== ИЗБРАННОЕ ====================

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Списки избранного с inline-фильмами"""
    list_display = ['user', 'get_movies_count']
    search_fields = ['user__username']
    inlines = [FavoriteMovieInline]

    def get_movies_count(self, obj):
        return obj.favoritemovie_set.count()
    get_movies_count.short_description = 'Фильмов'


@admin.register(FavoriteMovie)
class FavoriteMovieAdmin(admin.ModelAdmin):
    """Фильмы в избранном"""
    list_display = ['favorite', 'movie']
    raw_id_fields = ['favorite', 'movie']


# ==================== ИСТОРИЯ ====================

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    """История просмотров"""
    list_display = ['user', 'movie', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['user__username', 'movie__movie_name']
    readonly_fields = ['viewed_at']
    raw_id_fields = ['user', 'movie']
