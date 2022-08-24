from rest_framework import permissions


class IsChatOwner(permissions.BasePermission):
    """
    Если профиль пользователя.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True
        return obj.user.id == request.user.id

