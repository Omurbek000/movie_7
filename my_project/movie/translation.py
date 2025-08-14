from modeltranslation.translator import TranslationOptions,register
from .models import Director, Actor, Genre, Movie, Country

@register(Director)
class DirectorTranslationOptions(TranslationOptions):
    fields = ('director_name', 'director_bio')


@register(Actor)
class DirectorTranslationOptions(TranslationOptions):
    fields = ('actor_name', 'actor_bio')


@register(Genre)
class DirectorTranslationOptions(TranslationOptions):
    fields = ('genre_name',)


@register(Country)
class DirectorTranslationOptions(TranslationOptions):
    fields = ('country_name',)


@register(Movie)
class DirectorTranslationOptions(TranslationOptions):
    fields = ('movie_name', 'descriptions')