from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Права доступа для администратора"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsModerator(permissions.BasePermission):
    """Права доступа для модератора"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator
