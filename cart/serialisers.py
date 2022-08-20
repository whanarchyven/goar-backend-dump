from rest_framework import serializers

from cart.models import Cart, CartProduct
from food.models import Product
from food.serialisers import ProductSerializer


class ProductAddSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

    def save(self, **kwargs):
        product_id = self.validated_data['product_id']
        product = Product.objects.get(id=product_id)
        cart = self.context["request"].user.cart
        CartProduct.objects.create(
            cart=cart,
            product=product
        )
        return cart

class ProductDeleteSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

    def save(self, **kwargs):
        product_id = self.validated_data['product_id']
        product = Product.objects.get(id=product_id)
        cart = self.context["request"].user.cart
        CartProduct.objects.filter(
            cart=cart,
            product=product
        ).delete()
        return cart

class ProductUpdateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    purchased = serializers.BooleanField()

    def save(self, **kwargs):
        product_id = self.validated_data['product_id']
        purchased = self.validated_data['purchased']
        product = Product.objects.get(id=product_id)
        cart = self.context["request"].user.cart
        cart_product = CartProduct.objects.filter(
            cart=cart,
            product=product
        ).first()
        cart_product.purchased = purchased
        cart_product.save()
        return cart


class CartProductUpdateSerializer(serializers.ModelSerializer):
    """Продукты в корзине, добавление, удаление, обновление."""

    class Meta:
        model = CartProduct
        fields = ['cart', 'product', 'purchased']


class CartProductSerializer(serializers.ModelSerializer):
    """Продукты в корзине."""
    product = ProductSerializer()

    class Meta:
        model = CartProduct
        fields = ['product', 'purchased']


class CartSerializer(serializers.ModelSerializer):
    """Корзина."""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    items = CartProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items']
