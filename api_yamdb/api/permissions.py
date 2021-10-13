from django.conf import settings
from rest_framework import permissions

METHOD_FOR_AUTHORS = ["PUT", "PATCH", "DELETE"]
ELEV_ROLE = [settings.ROLE_ADMIN, settings.ROLE_MODERATOR]


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == settings.ROLE_ADMIN
            or request.user.is_superuser
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.role == settings.ROLE_ADMIN
        )


class ReviewCommentsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.role in ELEV_ROLE:
            return True
        if request.method in METHOD_FOR_AUTHORS and request.user != obj.author:
            return False
        return True
