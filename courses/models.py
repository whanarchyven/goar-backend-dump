from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class CourseDay(models.Model):
    """День курса."""
    number = models.PositiveIntegerField("Номер дня")
    date_of_day = models.DateField("Дата")

    def __str__(self):
        return f" День {self.number}"

    class Meta:
        verbose_name = "День курса"
        verbose_name_plural = "Дни курса"


class Task(models.Model):
    """Задачи для дня курса."""
    course_day = models.ForeignKey(
        CourseDay,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    name = models.CharField("Задача", max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Задача на день"
        verbose_name_plural = "Задачи на день"


class CourseDayTaskUser(models.Model):
    """Статус выполнения"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_status")
    course_day = models.ForeignKey(CourseDay, on_delete=models.CASCADE, related_name="task_status")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_status")

