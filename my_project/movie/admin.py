from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin


class MovieMomentsInline(admin.TabularInline):
    model = Moments
    extra = 1

class MovieLanguageInline(admin.TabularInline):
    model = MovieLanguage
    extra = 3



@admin.register(Movie)
class ProductAdmin(TranslationAdmin):
    inlines = [MovieLanguageInline, MovieMomentsInline]
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Country, Genre, Director, Actor)
class ProductAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


admin.site.register(Profile)
admin.site.register(Rating)
admin.site.register(Favorite)
admin.site.register(FavoriteMovie)
admin.site.register(History)