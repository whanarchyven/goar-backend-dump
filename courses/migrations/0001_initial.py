# Generated by Django 4.1 on 2022-08-22 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CourseDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(verbose_name='Номер дня')),
                ('date_of_day', models.DateField(verbose_name='Дата')),
            ],
            options={
                'verbose_name': 'День курса',
                'verbose_name_plural': 'Дни курса',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Задача')),
                ('course_day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='courses.courseday')),
            ],
            options={
                'verbose_name': 'Задача на день',
                'verbose_name_plural': 'Задачи на день',
            },
        ),
    ]