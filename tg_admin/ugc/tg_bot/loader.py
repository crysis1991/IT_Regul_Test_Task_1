from telebot import TeleBot
from loguru import logger
from telebot.storage import StateMemoryStorage
from .config_data.config import TgSettings


storage = StateMemoryStorage()
bot = TeleBot(token=TgSettings().BOT_TOKEN.get_secret_value(), state_storage=storage)
log = logger

log.add('debug.json',
        format='{time} | {level} | {message}',
        rotation='00:00',
        compression='zip',
        level='DEBUG',
        serialize=True)
log.add('info.json',
        format='{time} | {level} | {message}',
        rotation='00:00',
        compression='zip',
        level='INFO',
        serialize=True)
log.add('error.json',
        format='{time} | {level} | {message}',
        rotation='00:00',
        compression='zip',
        level='ERROR',
        serialize=True)
