from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = "Пользователи"

    def ready(self):
        from .signals import create_user_cart, log_user_logged_in_success

