from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from cart.models import Cart, CartProduct
from cart.permissions import IsCartOwner, IsCartProductOwner
from cart.serialisers import CartSerializer, CartProductUpdateSerializer, ProductAddSerializer, ProductDeleteSerializer, \
    ProductUpdateSerializer


class CartViewSet(mixins.ListModelMixin,
                  GenericViewSet):
    """
    Корзина. Выводит продукты в корзине пользователя.
    На выходе список, но должно отдавать только один элемент.
    """
    serializer_class = CartSerializer
    queryset = Cart.objects.prefetch_related('products')
    methods = ["post"]
    pagination_class = None
    permission_classes = [IsAuthenticated, IsCartOwner]

    def list(self, request, *args, **kwargs):
        self.queryset = Cart.objects.filter(id=request.user.cart.id).prefetch_related('products')
        return super().list(request, args, kwargs)

    @action(detail=False, methods=["post"],
            permission_classes=(IsAuthenticated, IsCartOwner),
            serializer_class=ProductAddSerializer)
    def add(self, request):
        """ Добавить продукт в корзину."""
        serializer = self.serializer_class(
            data={
                "product_id": request.data.get('product_id'),
            },
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        cart = serializer.save()
        cart_serializer = CartSerializer(instance=cart)
        return Response(status=status.HTTP_201_CREATED, data=cart_serializer.data)

    @action(detail=False, methods=["post"],
            permission_classes=(IsAuthenticated, IsCartOwner),
            serializer_class=ProductDeleteSerializer)
    def delete(self, request):
        """ Удалитиь продукт из корзины."""
        serializer = self.serializer_class(
            data={
                "product_id": request.data.get('product_id'),
            },
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        cart = serializer.save()
        cart_serializer = CartSerializer(instance=cart)
        return Response(status=status.HTTP_200_OK, data=cart_serializer.data)

    @action(detail=False, methods=["post"],
            permission_classes=(IsAuthenticated, IsCartOwner),
            url_path="update-status",
            serializer_class=ProductUpdateSerializer)
    def update_status(self, request):
        """ Обновить статус продукта в чек-листе (куплено-не куплено)."""
        serializer = self.serializer_class(
            data={
                "product_id": request.data.get('product_id'),
                "purchased": request.data.get('purchased')
            },
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        cart = serializer.save()
        cart_serializer = CartSerializer(instance=cart)
        return Response(status=status.HTTP_200_OK, data=cart_serializer.data)


class CartProductViewSet(ModelViewSet):
    """ Продукты в корзине.
    Добавление, удаление, изменение
    статуса продуктов в корзине."""
    serializer_class = CartProductUpdateSerializer
    queryset = CartProduct.objects.all()
    http_method_names = ("get", "patch", "delete", "post")
    permission_classes = [IsAuthenticated, IsCartProductOwner]
