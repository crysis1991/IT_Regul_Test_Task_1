from telebot.types import Message

from ...config_data.config import DEFAULT_COMMANDS
from ...loader import bot, log


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    """
    Выводим справку о командах бота
    :param message:
    :return:
    """
    log.debug('')
    log.info(f'user_id: {message.from_user.id}, chat_id: {message.chat.id}')
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text))
