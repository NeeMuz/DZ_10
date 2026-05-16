from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthorOrAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Всі користувачі можуть читати (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True

        # Для інших методів (POST, PUT, PATCH, DELETE) перевіряємо авторизацію
        if not request.user or not request.user.is_authenticated:
            return False

        # Адміністратори та модератори можуть редагувати та видаляти будь-які статті
        if request.user.is_superuser or request.user.is_staff:
            return True

        # Автор статті може редагувати та видаляти свою статтю
        return obj.author == request.user


class IsEditorsGroupOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Всі користувачі можуть читати (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True

        # Для інших методів (POST, PUT, PATCH, DELETE) перевіряємо авторизацію
        if not request.user or not request.user.is_authenticated:
            return False

        # Перевіряємо, чи користувач належить до групи "Editors"
        # is_editor = request.user.groups.filter(name='Editors').exists()

        # Адміністратори та модератори можуть редагувати та видаляти будь-які статті
        return request.user.is_superuser or request.user.is_staff or request.user.is_authenticated
