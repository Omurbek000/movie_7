from rest_framework import permissions


class CheckStatus(permissions.BasePermission):
    """Pro-пользователи видят весь контент. Simple — только простой (бесплатный)"""

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        # Pro-пользователи видят всё
        if request.user.is_authenticated and request.user.status == 'pro':
            return True
        # Simple и неавторизованные — только бесплатный контент
        if obj.status_movie == 'simple':
            return True
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Пользователь может редактировать только свои объекты"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user