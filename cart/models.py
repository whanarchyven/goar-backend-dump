from django.contrib.auth import get_user_model
from django.db import models

from food.models import Product

User = get_user_model()


class Cart(models.Model):
    """ Корзина. """
    user = models.OneToOneField(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name='cart'
    )
    products = models.ManyToManyField(Product, through="CartProduct")


class CartProduct(models.Model):
    """Продукт в корзине"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchased = models.BooleanField("Куплено", default=False)

    class Meta:
        unique_together = ['cart', 'product']
