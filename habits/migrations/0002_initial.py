# Generated by Django 5.1.2 on 2024-10-29 14:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('habits', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='habit',
            name='user',
            field=models.ForeignKey(help_text='Укажите владельца привычки', on_delete=django.db.models.deletion.CASCADE, related_name='habit_user', to=settings.AUTH_USER_MODEL, verbose_name='Владелец привычки'),
        ),
    ]