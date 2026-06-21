"""
Корневые URL-маршруты проекта movie_7.
- /admin/      — Django admin
- /docs/       — Swagger UI документация API
- /accounts/   — allauth (соцсети: Google, GitHub)
- /{lang}/...  — i18n маршруты приложения movie
"""
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Swagger/OpenAPI документация
schema_view = get_schema_view(
    openapi.Info(
        title="Movie Site API",
        description="API для сайта фильмов с рейтингами, избранным и историей просмотров",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('movie.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('accounts/', include('allauth.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)