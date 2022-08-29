from datetime import datetime

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

def _image_path(instance, filename):
    return 'user/{}/{}/{}/{}/{}'.format(
        datetime.now().strftime("%Y"),
        datetime.now().strftime("%m"),
        datetime.now().strftime("%d"),
        datetime.now().strftime("%H%M"),
        filename
    )

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class FitnessUser(AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    phone = models.CharField(
        "Телефон",
        max_length=15,
        unique=True,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Profile(models.Model):
    """Профиль пользователя."""
    user = models.OneToOneField(
        FitnessUser,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    weight = models.IntegerField("Вес", null=True, blank=True)
    waist_circumference = models.IntegerField("ОТ", null=True, blank=True)
    hip_circumference = models.IntegerField("ОБ", null=True, blank=True)
    chest_volume = models.IntegerField("ОГ", null=True, blank=True)
    target_weight = models.IntegerField("Цель по весу", null=True, blank=True)
    target_waist_circumference = models.IntegerField("Цель ОТ", null=True, blank=True)
    target_hip_circumference = models.IntegerField("Цель ОБ", null=True, blank=True)
    target_chest_volume = models.IntegerField("Цель ОГ", null=True, blank=True)
    profile_image = models.ImageField("Фото профиля", null=True, blank=True, upload_to=_image_path)
    photo_before = models.ImageField("Фото до", null=True, blank=True, upload_to=_image_path)
    photo_after = models.ImageField("Фото после", null=True, blank=True, upload_to=_image_path)
    daily_calorie_intake = models.IntegerField("Суточная норма ккал", null=True, blank=True)
    daily_water_intake = models.FloatField("Суточная норма воды, мл", null=True, blank=True)
    daily_step_rate = models.FloatField("Суточная норма шагов", null=True, blank=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профиль"

