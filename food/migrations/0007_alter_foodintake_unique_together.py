# Generated by Django 4.1 on 2022-09-01 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0006_alter_foodintake_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='foodintake',
            unique_together=set(),
        ),
    ]