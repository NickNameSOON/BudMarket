from django.core.management.base import BaseCommand
from telegram.ext import Application

class Command(BaseCommand):
    help = 'Run the Telegram bot'

    def handle(self, *args, **kwargs):
        from bot.bot import application
        application.run_polling()
