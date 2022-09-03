from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


def _video_path(instance, filename):
    return 'video/{}/{}/{}/{}/{}'.format(
        datetime.now().strftime("%Y"),
        datetime.now().strftime("%m"),
        datetime.now().strftime("%d"),
        datetime.now().strftime("%H%M"),
        filename
    )

def _image_path(instance, filename):
    return 'image/{}/{}/{}/{}/{}'.format(
        datetime.now().strftime("%Y"),
        datetime.now().strftime("%m"),
        datetime.now().strftime("%d"),
        datetime.now().strftime("%H%M"),
        filename
    )


class Training(models.Model):
    """Тренировка."""
    name = models.CharField("Название", max_length=500)
    video = models.FileField("Видео", upload_to=_video_path)
    calories_rating = models.PositiveIntegerField(
        "Оценка по калориям",
        help_text="от 0 до 5",
        default=5
    )
    training_time = models.PositiveIntegerField(
        "Время тренировки в минутах",
        default=60
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тренировка"
        verbose_name_plural = "Тренировки"


class TrainingFavorite(models.Model):
    """Избранные тренировки."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='training_favorites')
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name='favorites')

    def __str__(self):
        return self.training.name

    class Meta:
        verbose_name = "Избранная тренировка"
        verbose_name_plural = "Избранные тренировки"
        unique_together = ['user', 'training']


class Lecture(models.Model):
    """Лекция."""
    name = models.CharField("Название", max_length=500)
    description = models.TextField("Описание")
    video = models.FileField(
        "Видео",
        upload_to=_video_path,
        null=True,
        blank=True
    )
    image = models.FileField(
        "Изображение",
        upload_to=_image_path
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Лекция"
        verbose_name_plural = "Лекции"