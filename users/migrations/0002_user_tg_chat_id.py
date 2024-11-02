# Generated by Django 5.1.2 on 2024-11-01 13:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='tg_chat_id',
            field=models.CharField(
                blank=True,
                help_text='Укажите id чата в Телеграмм',
                max_length=255, null=True,
                verbose_name='id чата в Телеграмм'
            ),
        ),
    ]