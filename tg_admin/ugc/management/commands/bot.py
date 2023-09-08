from django.core.management.base import BaseCommand
from ...tg_bot.loader import bot, log
from ...tg_bot.utils.set_bot_commands import set_default_commands
from ...tg_bot import handlers  # noqa


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):

        log.info('Бот включен')
        set_default_commands(bot)
        bot.infinity_polling()
