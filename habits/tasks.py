import os
import django

from datetime import timedelta

from celery import shared_task
from django.utils import timezone
from config.settings import TG_BOT_TOKEN
from habits.models import Habit
from habits.services import send_telegram_reminder

# В связи с ошибкой добавлена переменная окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cw_drf.settings')

# Инициализация Django
django.setup()


@shared_task
def send_habit_reminders():
    """ Проверяем каждые 5 минут базу привычек, если привычка входит в нужный диапазон, тогда
        проверяем наличие телеграм id в habit.user.tg_chat_id
        если id есть, тогда
            проверяем отправлялось ли ранее напоминание, если нет, то отправляем в Telegram
            если нет, тогда сверяем периодичность 'frequency', если ок, то отправляем в Telegram

     Переменные: Токен Telegram берем из .env
     habit.user.tg_chat_id должен быть заведен вместе с пользователем, по-умолчанию поле **NULLABLE
     """

    current_time = timezone.localtime(timezone.now())
    time_lower_bound = (current_time - timedelta(minutes=5)).time()
    print('time_lower_bound:', time_lower_bound)
    time_upper_bound = (current_time + timedelta(minutes=5)).time()
    print('time_upper_bound:', time_upper_bound)

    # Получаем привычки с временем выполнения в пределах 5 минут от текущего времени
    habits = Habit.objects.filter(
        time__gte=time_lower_bound,
        time__lte=time_upper_bound
    )

    for habit in habits:
        print('habit:', habit)
        print('habit.user.tg_chat_id:', habit.user.tg_chat_id)
        if habit.user.tg_chat_id:
            last_reminder = habit.reminder_histories.order_by('-sent_at').first()

            # проверка частоты напоминаний и отправки первого напоминания
            if last_reminder is None or (last_reminder and timezone.now().date() == (
                    last_reminder.sent_at + timedelta(days=habit.frequency)).date()):
                message = f"Напоминание: Пора выполнить вашу привычку '{habit.action}'!"
                send_telegram_reminder(habit, message, telegram_token=TG_BOT_TOKEN, chat_id=habit.user.tg_chat_id)
                print('send_habit_reminders - is done')


if __name__ == '__main__':
    send_habit_reminders()
