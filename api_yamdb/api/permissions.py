from rest_framework import permissions
from reviews.models import User
from django.shortcuts import get_object_or_404

METHOD_FOR_AUTHORS = ['PUT', 'PATCH', 'DELETE']
ROLE = ['admin', 'moderator']


class ReviewCommentsPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.user.role in ROLE:
            return True
        if request.method in METHOD_FOR_AUTHORS and request.user != obj.author:
            return False
        return True


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user.is_authenticated and request.user.role == 'admin'
        )

