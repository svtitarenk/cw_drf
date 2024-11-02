from django.contrib import admin

from habits.models import Habit, ReminderHistory


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_filter = (
        'id', 'user',
        'place',
        'time',
        'action',
        'is_pleasant',
        'related_habit',
        'reward',
        'frequency',
        'estimated_time',
        'is_public',
    )


@admin.register(ReminderHistory)
class ReminderHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'habit',
        'sent_at',
        'delivery_status',
        'error_message',
    )
