from rest_framework import permissions


class IsFoodIntake(permissions.BasePermission):
    """
    Если это прием пищи пользователя.
    """
    def has_object_permission(self, request, view, obj):

        if request.user.is_admin:
            return True
        return obj.user.id == request.user.id


