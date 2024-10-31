from django.core.exceptions import ValidationError
from datetime import timedelta


def validate_reward_or_related_habit(habit):
    """ Исключает одновременное заполнение полей `reward` и `related_habit` """

    if habit.get("reward") and habit.get("related_habit"):
        raise ValidationError("Вы можете указать либо 'reward', либо 'related_habit', но не оба поля.")


def validate_duration(estimated_time):
    """ Ограничивает продолжительность выполнения привычки до 120 секунд """

    max_duration = timedelta(seconds=120)
    if estimated_time > max_duration:
        raise ValidationError("Время выполнения не должно превышать 120 секунд.")


def validate_related_habit_pleasant(habit):
    """ Связанной привычкой может быть только привычка с `is_pleasant=True` """

    if habit.get("related_habit") and not habit.get("related_habit").is_pleasant:
        raise ValidationError("Связанной привычкой может быть только привычка с признаком 'is_pleasant=True'.")


def validate_pleasant_habit_constraints(habit):
    """ Для приятной привычки нельзя указывать `reward` или `related_habit` """

    if habit.get("is_pleasant") and (habit.get("reward") or habit.get("related_habit")):
        raise ValidationError("У приятной привычки не может быть 'reward' или 'related_habit'.")


def validate_frequency(frequency):
    """ Ограничение на частоту выполнения привычки """

    if frequency < 1 or frequency > 7:
        raise ValidationError("Привычка должна выполняться как минимум раз в неделю (частота от 1 до 7 дней).")
