from rest_framework import permissions


class IsCartOwner(permissions.BasePermission):
    """
    Если это корзина пользователя.
    """
    def has_object_permission(self, request, view, obj):

        if request.user.is_admin:
            return True
        return obj.id == request.user.cart.id


class IsCartProductOwner(permissions.BasePermission):
    """
    Если это корзина пользователя при добавлении удалении продуктов.
    """
    def has_permission(self, request, view):
        if request.user.is_admin:
            return True
        if request.method in permissions.SAFE_METHODS:
            return False
        return request.user.cart.id == request.data.get('cart')

    def has_object_permission(self, request, view, obj):
        if request.iser.is_admin:
            return True
        return request.user.cart.id == request.data.get('cart')

