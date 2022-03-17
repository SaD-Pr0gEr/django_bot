from django.core.management import BaseCommand


class Command(BaseCommand):
    """Команда запуска бота"""

    help = "Command for run bot"

    def handle(self, *args, **options):
        from main.bot.handlers import bot

        bot.infinity_polling()
