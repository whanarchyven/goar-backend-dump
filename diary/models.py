from django.contrib.auth import get_user_model
from django.db import models

from courses.models import CourseDay

User = get_user_model()


MOOD_TYPE = [
    ('great', 'Отлично'),
    ('bad', 'Плохо'),
    ('normally', 'Нормально'),
    ('appeasement', 'Умиротворение'),
]


class ClassDayDiary(models.Model):
    """Дневник занятий на каждый день курса."""
    course_day = models.ForeignKey(
        CourseDay,
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="День курса",
        related_name='dairy'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    mood = models.CharField(
        "Настроение",
        null=True, blank=True,
        max_length=100,
        choices=MOOD_TYPE
    )
    increased_activity = models.BooleanField(
        "Повышенная активность на протяжении дня",
        default=False
    )
    fasting_day = models.BooleanField(
        "Разгрузочный день",
        default=False
    )
    steps = models.BooleanField(
        "Шаги",
        default=False
    )
    training = models.BooleanField(
        "Тренировка",
        default=False
    )
    water = models.PositiveIntegerField(
        "Вода в мл",
         default=0
    )
    food = models.BooleanField(
        "Питание",
        default=False
    )
    weight = models.IntegerField("Вес", null=True, blank=True)
    waist_circumference = models.IntegerField("ОТ", null=True, blank=True)
    hip_circumference = models.IntegerField("ОБ", null=True, blank=True)
    chest_volume = models.IntegerField("ОГ", null=True, blank=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "Дневник"
        verbose_name_plural = "Дневники"
        unique_together = ['user', 'course_day']

