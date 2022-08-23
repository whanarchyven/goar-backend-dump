# Generated by Django 4.1 on 2022-08-19 12:48

from django.db import migrations, models
import training.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название')),
                ('video', models.FileField(upload_to=training.models._video_path, verbose_name='Видео')),
                ('calories_rating', models.PositiveIntegerField(default=0, help_text='от 0 до 5', verbose_name='Оценка по калориям')),
                ('training_time', models.PositiveIntegerField(default=0, verbose_name='Время тренировки в минутах')),
            ],
            options={
                'verbose_name': 'Тренировка',
                'verbose_name_plural': 'Тренировки',
            },
        ),
    ]