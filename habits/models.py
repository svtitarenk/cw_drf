from django.core.exceptions import ValidationError
from django.db import models
from datetime import timedelta

from users.models import User

NULLABLE = {"null": True, "blank": True}  # default


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='habit_user', verbose_name='Владелец привычки',
                             help_text='Укажите владельца привычки')
    place = models.CharField(max_length=255, verbose_name='Место', help_text='Введите место')
    time = models.TimeField(verbose_name='Время', help_text='Время выполнения')
    action = models.CharField(max_length=255, verbose_name='Действие', help_text='Введите действие')
    # Признак приятной привычки
    is_pleasant = models.BooleanField(default=False, verbose_name='Приятная привычка?',
                                      help_text='Это приятная привычка?')
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL,
                                      **NULLABLE, verbose_name='Связанная привычка',
                                      help_text='Если это полезная привычка, укажите вознаграждение',
                                      related_name='linked_habits')
    reward = models.CharField(max_length=255, **NULLABLE, verbose_name='Вознаграждение',
                              help_text='Если не указана связанная привычка, укажите вознаграждение')
    # Периодичность выполнения в днях
    frequency = models.IntegerField(default=1, verbose_name='Периодичность',
                                    help_text='Укажите периодичность (1 ежедневно)')
    estimated_time = models.DurationField(default=timedelta(minutes=2),
                                          verbose_name='Продолжительность',
                                          help_text="Сколько будет длиться выполнение")
    is_public = models.BooleanField(default=False)  # Признак публичности

    def __str__(self):
        return f"{self.user}'s habit: {self.action}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
