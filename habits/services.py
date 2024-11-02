import requests
from django.utils import timezone
from config import settings
from habits.models import ReminderHistory


def send_telegram_reminder(habit, message, telegram_token, chat_id):
    url = f"{settings.TELEGRAM_URL}{settings.TG_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()

        # Создание записи об успешной отправке
        ReminderHistory.objects.create(
            habit=habit,
            sent_at=timezone.now(),
            delivery_status='sent'
        )
    except requests.RequestException as e:
        # Создание записи при неудачной отправке
        ReminderHistory.objects.create(
            habit=habit,
            sent_at=timezone.now(),
            delivery_status='failed',
            error_message=str(e)
        )
