from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from habits.models import Habit
from habits.validators import (validate_reward_or_related_habit,
                               validate_pleasant_habit_constraints,
                               validate_duration,
                               validate_related_habit_pleasant,
                               validate_frequency)


class HabitSerializer(serializers.ModelSerializer):
    email = SerializerMethodField()
    related_habit_action = serializers.CharField(source="related_habit.action", read_only=True)
    habit_user_chat_id = serializers.CharField(source="habit.habit_user.tg_chat_id", read_only=True)

    class Meta:
        model = Habit
        fields = [
            'id', 'email', 'habit_user_chat_id', 'place', 'time', 'action', 'related_habit_action', 'is_pleasant',
            'related_habit', 'reward', 'frequency', 'estimated_time', 'is_public'
        ]

    def get_email(self, obj):
        return obj.user.email

    def validate(self, data):
        """ Исключает одновременное заполнение полей reward и related_habit """
        validate_reward_or_related_habit(data)
        validate_pleasant_habit_constraints(data)

        # Проверяем ограничения продолжительности выполнения
        validate_duration(data['estimated_time'])

        # Проверка, что `related_habit` может быть только приятной привычкой
        if 'related_habit' in data:
            validate_related_habit_pleasant(data)

        # Проверка, что частота в пределах 1-7 дней
        validate_frequency(data['frequency'])

        return data


class PublicHabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            'id', 'place', 'time', 'action', 'is_pleasant', 'reward', 'frequency', 'estimated_time'
        ]
