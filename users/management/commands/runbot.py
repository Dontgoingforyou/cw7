from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from asgiref.sync import sync_to_async

from users.models import Profile


class Command(BaseCommand):
    help = 'Запуск Telegram-бота'

    def handle(self, *args, **kwargs):

        @sync_to_async
        def ensure_profile(user):
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)
            return user.profile

        @sync_to_async
        def get_user_by_email(email):
            try:
                return User.objects.get(email=email)
            except User.DoesNotExist:
                return None

        async def start(update: Update, context: CallbackContext):
            await update.message.reply_text("Привет! Я бот, и я работаю.")
            telegram_id = update.effective_user.id
            email = context.args[0] if context.args else None

            if email:
                user = await get_user_by_email(email)
                if user:
                    profile = await ensure_profile(user)
                    profile.telegram_id = telegram_id
                    await sync_to_async(profile.save)()
                    await update.message.reply_text(f"Ваш Telegram ID привязан к аккаунту {user.username}.")
                else:
                    await update.message.reply_text("Пользователь с указанным email не найден.")
            else:
                await update.message.reply_text("Email не был предоставлен.")

        application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.run_polling()