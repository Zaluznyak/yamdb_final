from rest_framework import permissions


class IsAuthorOrStaffOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        sufficient_conditions = (
            obj.author == user,
            user.is_admin,
            user.is_staff,
            user.is_moderator,
            user.is_superuser,
        )
        return any(sufficient_conditions)


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        sufficient_conditions = (
            request.method in permissions.SAFE_METHODS,
            user.is_staff,
            user.is_superuser,
        )
        return any(sufficient_conditions)
