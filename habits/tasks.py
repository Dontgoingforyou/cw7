from celery import shared_task
from telegram import Bot
from django.conf import settings

from habits.models import Habit


@shared_task
def send_telegram_reminder(habit_id):
    habit = Habit.objects.get(id=habit_id)
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    message = f'Напоминание о привычке {habit.action} в {habit.place} в {habit.time}.'
    bot.send_message(chat_id=habit.user.profile.telegram_id, text=message)
