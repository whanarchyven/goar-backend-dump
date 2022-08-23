from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from cart.models import Cart
from users.models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    Cart.objects.get_or_create(user=instance)
    Profile.objects.get_or_create(user=instance)