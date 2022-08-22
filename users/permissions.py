from rest_framework import permissions


class IsProfileOwner(permissions.BasePermission):
    """
    Если профиль пользователя.
    """
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.profile.id

