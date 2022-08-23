# Generated by Django 4.1 on 2022-08-22 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseDayTaskUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_status', to='courses.courseday')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_status', to='courses.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_status', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]