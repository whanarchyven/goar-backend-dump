# Generated by Django 4.1 on 2022-08-23 12:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0003_courseday_tip_of_the_day'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassDayDiary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mood', models.CharField(blank=True, choices=[('great', 'Отлично'), ('bad', 'Плохо'), ('normally', 'Нормально'), ('appeasement', 'Умиротворение')], max_length=100, null=True, verbose_name='Настроение')),
                ('increased_activity', models.BooleanField(default=False, verbose_name='Повышенная активность на протяжении дня')),
                ('fasting_day', models.BooleanField(default=False, verbose_name='Разгрузочный день')),
                ('steps', models.BooleanField(default=False, verbose_name='Шаги')),
                ('training', models.BooleanField(default=False, verbose_name='Тренировка')),
                ('water', models.BooleanField(default=False, verbose_name='Вода')),
                ('food', models.BooleanField(default=False, verbose_name='Питание')),
                ('weight', models.IntegerField(blank=True, null=True, verbose_name='Вес')),
                ('waist_circumference', models.IntegerField(blank=True, null=True, verbose_name='ОТ')),
                ('hip_circumference', models.IntegerField(blank=True, null=True, verbose_name='ОБ')),
                ('chest_volume', models.IntegerField(blank=True, null=True, verbose_name='ОГ')),
                ('course_day', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.courseday', verbose_name='День курса')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Дневник',
                'verbose_name_plural': 'Дневники',
            },
        ),
    ]
